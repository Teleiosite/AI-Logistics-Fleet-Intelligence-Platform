from app.tasks.celery_app import celery_app


@celery_app.task(name="notifications.send_email")
def send_email_notification(recipient: str, subject: str, message: str) -> dict[str, str]:
    # Placeholder task. Replace with SendGrid/SES integration in production.
    return {"recipient": recipient, "subject": subject, "status": "queued"}


@celery_app.task(name="notifications.send_sms")
def send_sms_notification(phone: str, message: str) -> dict[str, str]:
    # Placeholder task. Replace with Twilio/Africa's Talking integration in production.
    return {"phone": phone, "status": "queued"}
