#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-$ROOT_DIR/.env}"
COMPOSE_FILE="$ROOT_DIR/infra/compose/docker-compose.yml"
COMPOSE_CMD=(docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE")

REFRESH_WEBHOOK="${REFRESH_WEBHOOK:-1}"
TELEGRAM_WEBHOOK_SECRET="${TELEGRAM_WEBHOOK_SECRET:-}"

echo "Resetting containers..."
"${COMPOSE_CMD[@]}" down
"${COMPOSE_CMD[@]}" up --build -d

echo "Running migrations..."
"${COMPOSE_CMD[@]}" run --rm api alembic upgrade head

if [[ "$REFRESH_WEBHOOK" == "1" ]]; then
  if [[ -n "${TELEGRAM_BOT_TOKEN:-}" ]]; then
    if command -v cloudflared >/dev/null 2>&1; then
      echo "Refreshing Telegram webhook via Cloudflare Tunnel..."
      pkill -f cloudflared >/dev/null 2>&1 || true
      LOG_FILE="/tmp/cloudflared.log"
      nohup cloudflared tunnel --url http://localhost:8000 --no-autoupdate > "$LOG_FILE" 2>&1 &
      sleep 4
      TUNNEL_URL=$(python3 - <<'PY'
import re
from pathlib import Path

log_path = Path("/tmp/cloudflared.log")
if not log_path.exists():
    print("", end="")
    raise SystemExit(0)

text = log_path.read_text()
match = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", text)
print(match.group(0) if match else "", end="")
PY
)
      if [[ -n "$TUNNEL_URL" ]]; then
        WEBHOOK_URL="$TUNNEL_URL/webhooks/telegram"
        if [[ -n "$TELEGRAM_WEBHOOK_SECRET" ]]; then
          curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
            -H "Content-Type: application/json" \
            -d "{\"url\":\"$WEBHOOK_URL\",\"secret_token\":\"$TELEGRAM_WEBHOOK_SECRET\"}" >/dev/null
        else
          curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
            -H "Content-Type: application/json" \
            -d "{\"url\":\"$WEBHOOK_URL\"}" >/dev/null
        fi
        echo "Webhook actualizado: $WEBHOOK_URL"
      else
        echo "No se pudo obtener la URL del tunnel. Revisa $LOG_FILE"
      fi
    else
      echo "cloudflared no esta instalado. Omite refresh de webhook."
    fi
  else
    echo "TELEGRAM_BOT_TOKEN no definido. Omite refresh de webhook."
  fi
fi

echo "Listo."
