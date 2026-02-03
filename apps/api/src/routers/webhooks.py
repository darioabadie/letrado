import os
from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models import Prompt, Response, User
from ..schemas import GoalEnum, TelegramUpdate, WebhookAccepted, WhatsAppWebhookIn
from ..services.seed import seed_user_words


router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/whatsapp", response_model=WebhookAccepted)
def whatsapp_webhook(
    payload: WhatsAppWebhookIn,
    db: Session = Depends(get_db),
    webhook_secret: str | None = Header(default=None, alias="X-Webhook-Secret"),
) -> WebhookAccepted:
    expected_secret = os.getenv("WHATSAPP_WEBHOOK_SECRET")
    if expected_secret and webhook_secret != expected_secret:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid webhook secret")

    user = db.query(User).filter(User.whatsapp_id == payload.from_id).first()
    if not user:
        user = User(
            whatsapp_id=payload.from_id,
            name=None,
            goal=GoalEnum.professional.value,
            timezone="UTC",
        )
        db.add(user)
        db.flush()
        seed_user_words(db, user.id, user.goal)

    prompt = (
        db.query(Prompt)
        .filter(Prompt.user_id == user.id)
        .order_by(Prompt.scheduled_for.desc())
        .first()
    )
    if not prompt:
        prompt = Prompt(
            user_id=user.id,
            content="Mensaje inicial",
            scheduled_for=payload.timestamp,
        )
        db.add(prompt)
        db.flush()

    response = Response(
        user_id=user.id,
        prompt_id=prompt.id,
        content=payload.message,
        is_valid=False,
    )
    db.add(response)
    db.commit()
    return WebhookAccepted()


def _send_telegram_message(chat_id: int, text: str) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        httpx.post(url, json={"chat_id": chat_id, "text": text}, timeout=5.0)
    except httpx.HTTPError:
        return


@router.post("/telegram", response_model=WebhookAccepted)
def telegram_webhook(
    payload: TelegramUpdate,
    db: Session = Depends(get_db),
    webhook_secret: str | None = Header(default=None, alias="X-Telegram-Bot-Api-Secret-Token"),
) -> WebhookAccepted:
    expected_secret = os.getenv("TELEGRAM_WEBHOOK_SECRET")
    if expected_secret and webhook_secret != expected_secret:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid webhook secret")

    message = payload.message
    if not message or not message.text:
        return WebhookAccepted()

    chat_id = message.chat.id
    external_id = str(chat_id)
    user = db.query(User).filter(User.whatsapp_id == external_id).first()
    if not user:
        user = User(
            whatsapp_id=external_id,
            name=message.chat.first_name,
            goal=GoalEnum.professional.value,
            timezone="UTC",
        )
        db.add(user)
        db.flush()
        seed_user_words(db, user.id, user.goal)

    prompt = (
        db.query(Prompt)
        .filter(Prompt.user_id == user.id)
        .order_by(Prompt.scheduled_for.desc())
        .first()
    )
    if not prompt:
        scheduled_for = datetime.fromtimestamp(message.date, tz=timezone.utc).replace(tzinfo=None)
        prompt = Prompt(
            user_id=user.id,
            content="Mensaje inicial",
            scheduled_for=scheduled_for,
        )
        db.add(prompt)
        db.flush()

    response = Response(
        user_id=user.id,
        prompt_id=prompt.id,
        content=message.text,
        is_valid=False,
    )
    db.add(response)
    db.commit()

    _send_telegram_message(chat_id, "Gracias, recibido.")
    return WebhookAccepted()
