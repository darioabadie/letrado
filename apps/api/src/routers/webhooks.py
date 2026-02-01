from fastapi import APIRouter

from ..schemas import WebhookAccepted, WhatsAppWebhookIn


router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/whatsapp", response_model=WebhookAccepted)
def whatsapp_webhook(payload: WhatsAppWebhookIn) -> WebhookAccepted:
    _ = payload
    return WebhookAccepted()
