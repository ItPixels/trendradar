"""Billing API endpoints."""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.billing.stripe_client import stripe_client
from app.billing.webhooks import construct_event, handle_webhook_event
from app.billing.plans import PLANS

router = APIRouter()


class CheckoutRequest(BaseModel):
    plan: str
    success_url: str = "http://localhost:3000/settings/billing?success=true"
    cancel_url: str = "http://localhost:3000/settings/billing?canceled=true"


@router.get("/plans")
async def list_plans():
    """Get all available plans."""
    return {
        "plans": [
            {
                "slug": slug,
                "name": plan["name"],
                "price_monthly": plan["price_monthly"],
                "limits": plan["limits"],
            }
            for slug, plan in PLANS.items()
        ]
    }


@router.post("/checkout")
async def create_checkout(data: CheckoutRequest):
    """Create a Stripe checkout session."""
    plan = PLANS.get(data.plan)
    if not plan or not plan.get("stripe_price_id"):
        raise HTTPException(status_code=400, detail="Invalid plan")

    # TODO: Get customer_id from authenticated user
    # For now, create a new customer
    customer_id = await stripe_client.create_customer("demo@trendradar.io")

    checkout_url = await stripe_client.create_checkout_session(
        customer_id=customer_id,
        price_id=plan["stripe_price_id"],
        success_url=data.success_url,
        cancel_url=data.cancel_url,
    )

    return {"url": checkout_url}


@router.post("/portal")
async def create_portal():
    """Create a Stripe customer portal session."""
    # TODO: Get customer_id from authenticated user
    portal_url = await stripe_client.create_portal_session(
        customer_id="cus_demo",
        return_url="http://localhost:3000/settings/billing",
    )
    return {"url": portal_url}


@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        event = construct_event(payload, sig_header)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

    result = await handle_webhook_event(event)
    return result
