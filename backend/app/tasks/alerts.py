"""Alert checking and notification tasks."""
import logging
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.alerts.check_alerts")
def check_alerts():
    """Check all active alerts against current trends."""
    logger.info("Checking alerts against current trends...")

    # TODO: Fetch active alerts and check against trending topics
    # alerts = fetch_active_alerts()
    # trends = fetch_current_trends(min_score=0)
    #
    # for alert in alerts:
    #     matching_trends = match_alert_to_trends(alert, trends)
    #     for trend in matching_trends:
    #         if not already_triggered(alert.id, trend.id):
    #             trigger_alert(alert, trend)

    return {"status": "completed"}


@celery_app.task(name="app.tasks.alerts.send_notification")
def send_notification(alert_id: str, trend_id: str, channels: list[str]):
    """Send alert notification through specified channels."""
    logger.info(f"Sending notification for alert {alert_id}, trend {trend_id} via {channels}")

    # TODO: Implement notification sending
    # for channel in channels:
    #     if channel == "email":
    #         send_email_notification(alert, trend)
    #     elif channel == "push":
    #         send_push_notification(alert, trend)
    #     elif channel == "telegram":
    #         send_telegram_notification(alert, trend)
    #     elif channel == "webhook":
    #         send_webhook_notification(alert, trend)

    return {"status": "sent", "channels": channels}
