import base64
import smtplib
from email.message import EmailMessage
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app.tasks.celery_app import celery_app
from app.core.config import get_settings


@celery_app.task(
    name="notifications.send_email",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=5,
)
def send_email_notification(recipient: str, subject: str, message: str) -> dict[str, str]:
    settings = get_settings()
    if not all((settings.smtp_host, settings.smtp_from_email)):
        raise RuntimeError("SMTP_HOST and SMTP_FROM_EMAIL must be configured for email notifications")

    email = EmailMessage()
    email["From"] = settings.smtp_from_email
    email["To"] = recipient
    email["Subject"] = subject
    email.set_content(message)
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as client:
        if settings.smtp_use_tls:
            client.starttls()
        if settings.smtp_username:
            if not settings.smtp_password:
                raise RuntimeError("SMTP_PASSWORD is required when SMTP_USERNAME is configured")
            client.login(settings.smtp_username, settings.smtp_password)
        client.send_message(email)
    return {"recipient": recipient, "subject": subject, "status": "sent"}


@celery_app.task(
    name="notifications.send_sms",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=5,
)
def send_sms_notification(phone: str, message: str) -> dict[str, str]:
    settings = get_settings()
    if not all((settings.twilio_account_sid, settings.twilio_auth_token, settings.twilio_from_number)):
        raise RuntimeError(
            "TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_FROM_NUMBER "
            "must be configured for SMS notifications"
        )

    endpoint = (
        f"https://api.twilio.com/2010-04-01/Accounts/"
        f"{settings.twilio_account_sid}/Messages.json"
    )
    credentials = base64.b64encode(
        f"{settings.twilio_account_sid}:{settings.twilio_auth_token}".encode()
    ).decode()
    request = Request(
        endpoint,
        data=urlencode({"To": phone, "From": settings.twilio_from_number, "Body": message}).encode(),
        headers={"Authorization": f"Basic {credentials}"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=15) as response:
            if response.status >= 300:
                raise RuntimeError(f"Twilio returned HTTP {response.status}")
    except HTTPError as exc:
        raise RuntimeError(f"Twilio returned HTTP {exc.code}") from exc
    return {"phone": phone, "status": "sent"}
