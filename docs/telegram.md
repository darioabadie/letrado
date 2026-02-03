# Integracion Telegram (Webhook)

Guia rapida para integrar Telegram como canal principal del MVP.

## Requisitos

- Bot creado con @BotFather.
- `TELEGRAM_BOT_TOKEN`.
- Webhook publico HTTPS (Cloudflare Tunnel recomendado).

## Variables de entorno

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_WEBHOOK_SECRET` (opcional)

## Webhook

Configura el webhook con tu URL publica:

```bash
curl -s -X POST "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://<PUBLIC_URL>/webhooks/telegram",
    "secret_token": "<TELEGRAM_WEBHOOK_SECRET>"
  }'
```

Verificar estado:

```bash
curl -s "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/getWebhookInfo"
```

## Onboarding esperado

1) Usuario envia `/start`.
2) Bot pide objetivo (Profesional/Academico/Creativo).
3) Bot pide hora (0-23).
4) Se siembra el preset y se confirma.

## Tunnel rapido (Cloudflare)

```bash
cloudflared tunnel --url http://localhost:8000
```

Usa la URL HTTPS entregada en el webhook.
