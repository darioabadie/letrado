# Arquitectura

Este documento describe la arquitectura de Letrado, los servicios, el flujo de datos y las decisiones tecnicas base para el MVP.

## Objetivo

Letrado es un SaaS B2C orientado a mejorar el vocabulario activo en hablantes nativos de espanol. La experiencia principal se vive en WhatsApp, mientras el backend procesa el lenguaje y un dashboard web muestra metricas.

Documentacion de la API: `docs/api.md`.
Guia de integracion Telegram: `docs/telegram.md`.

## Arquitectura general

**Canal**

- WhatsApp Business Cloud API como interfaz principal.

**Servicios**

- `api` (FastAPI): entrypoint HTTP, webhooks, logica de negocio, lectura/escritura de datos.
- `worker` (Celery): tareas asincronas (evaluacion semantica, NLP, metricas).
- `scheduler` (Celery beat): jobs periodicos (prompts diarios).
- `db` (PostgreSQL + pgvector): datos core y memoria semantica.
- `redis`: broker y cache para Celery.
- `dashboard` (Next.js): visualizacion de metricas e historiales.

## Flujo de datos (alto nivel)

1) Usuario recibe un prompt diario via WhatsApp.
2) Usuario responde en texto (y luego voz) y el webhook llega a `api`.
3) `api` persiste la respuesta y dispara tareas en `worker`.
4) `worker` valida lemas, evalua contexto, genera feedback y actualiza estados.
5) `dashboard` consume metricas y conversaciones procesadas desde `api`.

## Base de datos (MVP)

Tablas iniciales:

- `users`: usuarios, objetivo y metadata basica.
- `words`: catalogo de palabras.
- `user_words`: relacion usuario-palabra con estado y conteos.
- `prompts`: prompts generados y enviados.
- `responses`: respuestas del usuario con feedback y validacion.
- `streaks`: rachas por usuario.
- `ttr_metrics`: metricas de riqueza lexica.

Migracion inicial:

- `apps/api/alembic/versions/0001_init_schema.py`

## Escalabilidad

- Servicios desacoplados via colas (Celery + Redis).
- Escalado horizontal de `worker` y `api`.
- DB optimizable con indices y particionado futuro.

## Seguridad y cumplimiento

- GDPR: datos cifrados en reposo y en transito.
- Secrets via variables de entorno.
- Logs sin contenido sensible.

## Observabilidad

- Logs estructurados en `api` y `worker`.
- Metricas basicas de latencia y tiempos de respuesta.

## Despliegue

- Todo containerizado con Docker y docker-compose.
- Despliegue portable a cualquier nube.
