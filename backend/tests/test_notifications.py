from types import SimpleNamespace

from app.tasks import notifications


def test_email_notification_sends_via_configured_smtp(monkeypatch) -> None:
    sent = []

    class FakeSMTP:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def starttls(self):
            sent.append("tls")

        def login(self, username, password):
            sent.append(("login", username, password))

        def send_message(self, message):
            sent.append(message)

    monkeypatch.setattr(notifications, "smtplib", SimpleNamespace(SMTP=FakeSMTP))
    monkeypatch.setattr(
        notifications,
        "get_settings",
        lambda: SimpleNamespace(
            smtp_host="smtp.example.test",
            smtp_port=587,
            smtp_username="user",
            smtp_password="password",
            smtp_from_email="no-reply@example.test",
            smtp_use_tls=True,
        ),
    )

    result = notifications.send_email_notification.run("recipient@example.test", "Subject", "Body")

    assert result == {"recipient": "recipient@example.test", "subject": "Subject", "status": "sent"}
    assert sent[0] == "tls"
    assert sent[1] == ("login", "user", "password")
    assert sent[2]["To"] == "recipient@example.test"


def test_sms_notification_posts_to_twilio(monkeypatch) -> None:
    captured = {}

    class FakeResponse:
        status = 201

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    def fake_urlopen(request, timeout):
        captured["request"] = request
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(notifications, "urlopen", fake_urlopen)
    monkeypatch.setattr(
        notifications,
        "get_settings",
        lambda: SimpleNamespace(
            twilio_account_sid="AC123",
            twilio_auth_token="token",
            twilio_from_number="+10000000000",
        ),
    )

    result = notifications.send_sms_notification.run("+10000000001", "Delivery update")

    assert result == {"phone": "+10000000001", "status": "sent"}
    assert captured["timeout"] == 15
    assert captured["request"].full_url.endswith("/Accounts/AC123/Messages.json")
