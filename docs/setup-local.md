# Setup local

Guia rapida para levantar el stack local con Docker Compose.

## Requisitos

- Docker 24+ (con Docker Compose v2)

## Levantar servicios

```bash
docker compose --env-file .env -f infra/compose/docker-compose.yml up --build
```

Servicios expuestos:

- API: `http://localhost:8000`
- Dashboard: `http://localhost:3000`
- Postgres: `localhost:5432`
- Redis: `localhost:6379`

## Migraciones

Ejecuta Alembic dentro del contenedor de `api`:

```bash
docker compose --env-file .env -f infra/compose/docker-compose.yml run --rm api alembic upgrade head
```

## Variables de entorno (local)

Para desarrollo local, `infra/compose/docker-compose.yml` ya incluye valores por defecto. Variables opcionales:

- `WHATSAPP_WEBHOOK_SECRET`
- `LLM_PROVIDER`
- `LLM_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_WEBHOOK_SECRET`

## Comandos utiles

Parar servicios (sin borrar datos):

```bash
docker compose --env-file .env -f infra/compose/docker-compose.yml down
```

Borrar volumenes (reset local):

```bash
docker compose --env-file .env -f infra/compose/docker-compose.yml down -v
```

Ver logs del API:

```bash
docker compose --env-file .env -f infra/compose/docker-compose.yml logs -f api
```

## Tests (API)

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r apps/api/requirements.txt -r apps/api/requirements-dev.txt
python3 -m pytest -c apps/api/pytest.ini
```
