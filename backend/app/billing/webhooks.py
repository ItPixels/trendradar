"""Stripe webhook handler."""
import stripe
import logging
from app.config import settings

logger = logging.getLogger(__name__)

def construct_event(payload: bytes, sig_header: str) -> stripe.Event:
    """Construct and verify a Stripe webhook event."""
    return stripe.Webhook.construct_event(
        payload, sig_header, settings.stripe_webhook_secret
    )

async def handle_webhook_event(event: stripe.Event) -> dict:
    """Handle a verified Stripe webhook event."""
    event_type = event["type"]
    data = event["data"]["object"]

    handlers = {
        "checkout.session.completed": _handle_checkout_completed,
        "customer.subscription.updated": _handle_subscription_updated,
        "customer.subscription.deleted": _handle_subscription_deleted,
        "invoice.payment_succeeded": _handle_payment_succeeded,
        "invoice.payment_failed": _handle_payment_failed,
    }

    handler = handlers.get(event_type)
    if handler:
        return await handler(data)

    logger.info(f"Unhandled webhook event: {event_type}")
    return {"status": "ignored", "event": event_type}


async def _handle_checkout_completed(data: dict) -> dict:
    """Handle successful checkout — activate subscription."""
    customer_id = data.get("customer")
    subscription_id = data.get("subscription")
    logger.info(f"Checkout completed: customer={customer_id}, sub={subscription_id}")

    # TODO: Update user's subscription in database
    return {"status": "processed", "action": "subscription_activated"}


async def _handle_subscription_updated(data: dict) -> dict:
    """Handle subscription update (plan change, renewal)."""
    subscription_id = data.get("id")
    status = data.get("status")
    logger.info(f"Subscription updated: {subscription_id}, status={status}")

    # TODO: Update subscription status in database
    return {"status": "processed", "action": "subscription_updated"}


async def _handle_subscription_deleted(data: dict) -> dict:
    """Handle subscription cancellation."""
    subscription_id = data.get("id")
    logger.info(f"Subscription deleted: {subscription_id}")

    # TODO: Downgrade user to free plan
    return {"status": "processed", "action": "subscription_cancelled"}


async def _handle_payment_succeeded(data: dict) -> dict:
    """Handle successful payment."""
    return {"status": "processed", "action": "payment_succeeded"}


async def _handle_payment_failed(data: dict) -> dict:
    """Handle failed payment."""
    customer_id = data.get("customer")
    logger.warning(f"Payment failed for customer: {customer_id}")

    # TODO: Send notification to user, update subscription status
    return {"status": "processed", "action": "payment_failed"}
