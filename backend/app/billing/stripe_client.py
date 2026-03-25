"""Stripe integration for billing."""
import stripe
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

stripe.api_key = settings.stripe_secret_key

class StripeClient:
    """Stripe billing operations."""

    async def create_customer(self, email: str, name: Optional[str] = None) -> str:
        """Create a Stripe customer."""
        customer = stripe.Customer.create(email=email, name=name)
        return customer.id

    async def create_checkout_session(
        self,
        customer_id: str,
        price_id: str,
        success_url: str,
        cancel_url: str,
    ) -> str:
        """Create a Stripe Checkout session."""
        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session.url

    async def create_portal_session(self, customer_id: str, return_url: str) -> str:
        """Create a Stripe Customer Portal session."""
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url,
        )
        return session.url

    async def cancel_subscription(self, subscription_id: str) -> bool:
        """Cancel a subscription at period end."""
        try:
            stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True,
            )
            return True
        except stripe.error.StripeError as e:
            logger.error(f"Failed to cancel subscription: {e}")
            return False

    async def get_subscription(self, subscription_id: str) -> Optional[dict]:
        """Get subscription details."""
        try:
            sub = stripe.Subscription.retrieve(subscription_id)
            return {
                "id": sub.id,
                "status": sub.status,
                "current_period_end": sub.current_period_end,
                "cancel_at_period_end": sub.cancel_at_period_end,
                "plan": sub["items"]["data"][0]["price"]["id"] if sub["items"]["data"] else None,
            }
        except stripe.error.StripeError:
            return None


stripe_client = StripeClient()
