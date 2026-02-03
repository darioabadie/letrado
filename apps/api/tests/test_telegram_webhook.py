from datetime import datetime, timezone

from src.models import Response, User


def _payload(text: str | None = "Hola"):
    return {
        "update_id": 1,
        "message": {
            "message_id": 10,
            "date": int(datetime(2026, 2, 1, 9, 10, 0, tzinfo=timezone.utc).timestamp()),
            "chat": {"id": 123456, "type": "private", "first_name": "Ana"},
            "text": text,
        },
    }


def test_telegram_webhook_creates_user_and_response(client, db_session, monkeypatch):
    def fake_post(*args, **kwargs):
        class Fake:
            status_code = 200

            def json(self):
                return {"ok": True}

        return Fake()

    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "token")
    monkeypatch.setattr("src.routers.webhooks.httpx.post", fake_post)

    response = client.post("/webhooks/telegram", json=_payload())

    assert response.status_code == 200
    user = db_session.query(User).filter(User.whatsapp_id == "123456").first()
    assert user is not None
    stored = db_session.query(Response).filter(Response.user_id == user.id).first()
    assert stored is not None
    assert stored.content == "Hola"


def test_telegram_webhook_ignores_non_text(client, db_session):
    response = client.post("/webhooks/telegram", json=_payload(text=None))

    assert response.status_code == 200
    user = db_session.query(User).filter(User.whatsapp_id == "123456").first()
    assert user is None


def test_telegram_webhook_requires_secret(client, monkeypatch):
    monkeypatch.setenv("TELEGRAM_WEBHOOK_SECRET", "supersecret")

    response = client.post("/webhooks/telegram", json=_payload())

    assert response.status_code == 401
    assert response.json()["detail"] == "invalid webhook secret"
