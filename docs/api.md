# API Letrado

Documentacion de los endpoints actuales expuestos por `apps/api` (FastAPI).

## Base

- Base URL: `http://localhost:8000`
- Formato: JSON
- Fechas: ISO 8601 (ej: `2026-02-01T12:34:56Z`)

## Enums

- `goal`: `professional` | `academic` | `creative`
- `word_status`: `latent` | `practice` | `active`

## Health

### GET /health

Chequeo de salud del servicio.

**Ejemplo**

```bash
curl -s http://localhost:8000/health
```

```json
{
  "status": "ok"
}
```

## Usuarios

### POST /users

Crea un usuario. `whatsapp_id` debe ser unico. En el MVP se siembra un banco inicial de palabras segun `goal`.

**Request**

```json
{
  "whatsapp_id": "5491122334455",
  "name": "Ana",
  "goal": "professional",
  "timezone": "America/Argentina/Buenos_Aires"
}
```

**Response 201**

```json
{
  "id": "3e3c6f1b-82c5-4d45-8d8f-6b3a7926e9c7",
  "whatsapp_id": "5491122334455",
  "name": "Ana",
  "goal": "professional",
  "timezone": "America/Argentina/Buenos_Aires",
  "created_at": "2026-02-01T12:34:56Z"
}
```

**Errores**

- `409`: `whatsapp_id already exists`

### GET /users/{user_id}

Obtiene un usuario por id.

**Ejemplo**

```bash
curl -s http://localhost:8000/users/3e3c6f1b-82c5-4d45-8d8f-6b3a7926e9c7
```

**Errores**

- `404`: `user not found`

### PATCH /users/{user_id}

Actualiza campos opcionales de un usuario.

**Request**

```json
{
  "name": "Ana B.",
  "goal": "academic",
  "timezone": "America/Santiago"
}
```

**Errores**

- `404`: `user not found`

## Vocabulario

### POST /users/{user_id}/words

Agrega palabras al vocabulario del usuario. Normaliza a minusculas y evita duplicados.

**Request**

```json
{
  "words": ["Ambiguo", "perspicaz", "  " ]
}
```

**Response 201**

```json
{
  "created": [
    {"word_id": 12, "text": "ambiguo", "status": "latent"},
    {"word_id": 13, "text": "perspicaz", "status": "latent"}
  ]
}
```

**Errores**

- `404`: `user not found`

### GET /users/{user_id}/words

Lista palabras del usuario con su estado y conteo.

**Ejemplo**

```bash
curl -s http://localhost:8000/users/3e3c6f1b-82c5-4d45-8d8f-6b3a7926e9c7/words
```

**Response 200**

```json
[
  {
    "word_id": 12,
    "text": "ambiguo",
    "status": "latent",
    "correct_uses": 0,
    "last_used_at": null
  }
]
```

**Errores**

- `404`: `user not found`

### PATCH /users/{user_id}/words/{word_id}

Actualiza el estado o conteo de una palabra del usuario.

**Request**

```json
{
  "status": "practice",
  "correct_uses": 2
}
```

**Errores**

- `404`: `user word not found`
- `404`: `word not found`

## Prompts

Nota: los prompts tambien se generan automaticamente por el scheduler diario.

### POST /users/{user_id}/prompts

Crea un prompt programado para un usuario.

**Request**

```json
{
  "content": "Escribe una frase con la palabra 'ambiguo'",
  "scheduled_for": "2026-02-01T09:00:00Z"
}
```

**Response 201**

```json
{
  "id": 5,
  "content": "Escribe una frase con la palabra 'ambiguo'",
  "scheduled_for": "2026-02-01T09:00:00Z",
  "sent_at": null
}
```

**Errores**

- `404`: `user not found`

### GET /users/{user_id}/prompts

Lista prompts del usuario ordenados por `scheduled_for` descendente.

**Ejemplo**

```bash
curl -s http://localhost:8000/users/3e3c6f1b-82c5-4d45-8d8f-6b3a7926e9c7/prompts
```

**Errores**

- `404`: `user not found`

## Respuestas

### POST /users/{user_id}/responses

Registra una respuesta del usuario para un prompt existente.

**Request**

```json
{
  "prompt_id": 5,
  "content": "El informe es ambiguo y requiere mas datos."
}
```

**Response 201**

```json
{
  "id": 9,
  "prompt_id": 5,
  "is_valid": false,
  "feedback": null,
  "created_at": "2026-02-01T09:10:00Z"
}
```

**Errores**

- `404`: `user not found`
- `404`: `prompt not found`

### GET /users/{user_id}/responses

Lista respuestas del usuario ordenadas por `created_at` descendente.

**Ejemplo**

```bash
curl -s http://localhost:8000/users/3e3c6f1b-82c5-4d45-8d8f-6b3a7926e9c7/responses
```

**Errores**

- `404`: `user not found`

## Metricas

### GET /users/{user_id}/metrics/ttr

Obtiene el ultimo valor de TTR (Type-Token Ratio) del usuario.

**Ejemplo**

```bash
curl -s http://localhost:8000/users/3e3c6f1b-82c5-4d45-8d8f-6b3a7926e9c7/metrics/ttr
```

**Response 200**

```json
{
  "ttr": 0.42,
  "calculated_at": "2026-02-01T10:00:00Z"
}
```

**Errores**

- `404`: `user not found`
- `404`: `ttr metric not found`

## Webhooks

### POST /webhooks/whatsapp

Entrada de mensajes desde WhatsApp. Si el usuario no existe, se crea con `goal=professional`, `timezone=UTC` y se siembra el preset. Si `WHATSAPP_WEBHOOK_SECRET` esta configurado, requiere header `X-Webhook-Secret`.

**Request**

```json
{
  "from_id": "5491122334455",
  "message": "Hola, esta es mi respuesta",
  "timestamp": "2026-02-01T09:10:00Z"
}
```

**Response 200**

```json
{
  "status": "accepted"
}
```

**Errores**

- `401`: `invalid webhook secret`

### POST /webhooks/telegram

Entrada de mensajes desde Telegram. Si el usuario no existe, se crea con `goal=professional`, `timezone=UTC` y se siembra el preset. Si `TELEGRAM_WEBHOOK_SECRET` esta configurado, requiere header `X-Telegram-Bot-Api-Secret-Token`.

**Request**

```json
{
  "update_id": 1,
  "message": {
    "message_id": 10,
    "date": 1706788200,
    "chat": {
      "id": 123456,
      "type": "private",
      "first_name": "Ana"
    },
    "text": "Hola"
  }
}
```

**Response 200**

```json
{
  "status": "accepted"
}
```

**Errores**

- `401`: `invalid webhook secret`
