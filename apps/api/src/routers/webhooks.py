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
            onboarding_step="completed",
            preferred_hour=9,
            is_active=True,
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


def _intro_message() -> str:
    return (
        "Bienvenido a Letrado. Recibiras prompts diarios para activar tu vocabulario. "
        "Responde 2 pasos: objetivo y hora."
    )


def _help_message() -> str:
    return (
        "Comandos: /start, /help, /status, /goal, /hour, /stop, /resume. "
        "Para comenzar: /start."
    )


def _status_message(user: User) -> str:
    estado = "activo" if user.is_active else "pausado"
    step = user.onboarding_step or "sin_onboarding"
    return (
        f"Estado: {estado}. Objetivo: {user.goal}. Hora: {user.preferred_hour}. "
        f"Onboarding: {step}."
    )


def _parse_goal(text: str) -> str | None:
    normalized = text.strip().lower()
    mapping = {
        "profesional": GoalEnum.professional.value,
        "professional": GoalEnum.professional.value,
        "academico": GoalEnum.academic.value,
        "academic": GoalEnum.academic.value,
        "creativo": GoalEnum.creative.value,
        "creative": GoalEnum.creative.value,
        "literario": GoalEnum.creative.value,
    }
    return mapping.get(normalized)


def _parse_hour(text: str) -> int | None:
    try:
        value = int(text.strip())
    except ValueError:
        return None
    if 0 <= value <= 23:
        return value
    return None


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
    if not message:
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
            onboarding_step="awaiting_goal",
            preferred_hour=9,
            is_active=True,
        )
        db.add(user)
        db.commit()
        _send_telegram_message(chat_id, _intro_message())
        _send_telegram_message(chat_id, "Elige tu objetivo: Profesional, Academico o Creativo.")
        return WebhookAccepted()

    if not message.text:
        _send_telegram_message(chat_id, "Por ahora solo texto. Envia /help.")
        return WebhookAccepted()

    text = message.text.strip()
    command = text.split()[0].lower() if text.startswith("/") else None
    if command == "/start":
        user.onboarding_step = "awaiting_goal"
        user.is_active = True
        db.commit()
        _send_telegram_message(chat_id, _intro_message())
        _send_telegram_message(chat_id, "Elige tu objetivo: Profesional, Academico o Creativo.")
        return WebhookAccepted()
    if command == "/help":
        _send_telegram_message(chat_id, _help_message())
        if user.onboarding_step != "completed":
            _send_telegram_message(chat_id, "Elige tu objetivo: Profesional, Academico o Creativo.")
        return WebhookAccepted()
    if command == "/status":
        _send_telegram_message(chat_id, _status_message(user))
        return WebhookAccepted()
    if command == "/goal":
        user.onboarding_step = "awaiting_goal"
        db.commit()
        _send_telegram_message(chat_id, "Elige tu objetivo: Profesional, Academico o Creativo.")
        return WebhookAccepted()
    if command == "/hour":
        user.onboarding_step = "awaiting_hour"
        db.commit()
        _send_telegram_message(chat_id, "A que hora quieres recibir el prompt diario? (0-23)")
        return WebhookAccepted()
    if command == "/stop":
        user.is_active = False
        db.commit()
        _send_telegram_message(chat_id, "Listo. Prompts pausados. Usa /resume para reanudar.")
        return WebhookAccepted()
    if command == "/resume":
        user.is_active = True
        db.commit()
        _send_telegram_message(chat_id, "Listo. Prompts reanudados.")
        return WebhookAccepted()

    if user.onboarding_step == "awaiting_goal":
        goal = _parse_goal(text)
        if not goal:
            _send_telegram_message(
                chat_id,
                "Objetivo invalido. Responde con: Profesional, Academico o Creativo.",
            )
            return WebhookAccepted()
        user.goal = goal
        user.onboarding_step = "awaiting_hour"
        db.commit()
        _send_telegram_message(
            chat_id,
            "A que hora quieres recibir el prompt diario? (0-23)",
        )
        return WebhookAccepted()

    if user.onboarding_step == "awaiting_hour":
        hour = _parse_hour(text)
        if hour is None:
            _send_telegram_message(chat_id, "Hora invalida. Envia un numero entre 0 y 23.")
            return WebhookAccepted()
        user.preferred_hour = hour
        user.onboarding_step = "completed"
        user.is_active = True
        seed_user_words(db, user.id, user.goal)
        db.commit()
        _send_telegram_message(
            chat_id,
            "Listo. Te enviaremos un prompt diario. Puedes responder con cualquier texto.",
        )
        return WebhookAccepted()

    if user.onboarding_step and user.onboarding_step != "completed":
        _send_telegram_message(chat_id, "Completemos el onboarding. Responde a la ultima pregunta.")
        return WebhookAccepted()

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
        content=text,
        is_valid=False,
    )
    db.add(response)
    db.commit()

    _send_telegram_message(chat_id, "Recibido. Gracias.")
    return WebhookAccepted()
