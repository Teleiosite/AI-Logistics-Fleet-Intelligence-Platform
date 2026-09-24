from dataclasses import dataclass
from typing import Protocol


class ExternalIntegration(Protocol):
    name: str

    def healthcheck(self) -> bool:
        """Return whether the configured provider is reachable."""


@dataclass(frozen=True)
class IntegrationStatus:
    name: str
    configured: bool
    health: str


def configured_integrations(settings) -> list[IntegrationStatus]:
    integrations = [
        ("ocr", settings.ocr_provider_url),
        ("telematics", settings.telematics_webhook_secret),
        ("email", settings.smtp_host),
        ("sms", settings.twilio_account_sid),
    ]
    return [
        IntegrationStatus(name=name, configured=bool(value), health="configured" if value else "not_configured")
        for name, value in integrations
    ]
