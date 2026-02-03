# Plan de Desarrollo (Container-first + Open Source)

Este plan define la ruta de construcción para Letrado con un enfoque 100% containerizado, listo para desplegar en cualquier nube, y con estrategia open source.

## Decisiones base

- Stack backend: Python 3.12 + FastAPI
- Colas async: Celery + Redis
- Base de datos: PostgreSQL + pgvector
- Licencia open source: Apache-2.0

## Arquitectura containerizada

- **api** (FastAPI)
  - REST API y webhook de Telegram (WhatsApp pausado)
  - Lógica de negocio (usuarios, vocabulario, prompts, métricas)
- **worker** (Celery)
  - Evaluación semántica, feedback, TTR y tareas NLP
- **scheduler** (Celery beat)
  - Envío de prompts diarios
- **db** (PostgreSQL + pgvector)
  - Datos core y memoria semántica
- **cache/queue** (Redis)
  - Broker para Celery y caching
- **dashboard** (Next.js)
  - Panel de métricas y visualizaciones

## Estructura propuesta del repositorio

```
/apps
  /api
  /worker
  /scheduler
  /dashboard
/infra
  /docker
  /compose
/docs
/scripts
```

## Fases y entregables

### Fase 1 — Base containerizada

- Dockerfiles para api/worker/scheduler/dashboard
- docker-compose para desarrollo y producción
- .env.example
- Scripts de migración Alembic

### Fase 2 — MVP funcional

- Onboarding + vocabulario inicial
- Webhook Telegram (texto)
- Daily trigger
- Lematización + verificación de palabras requeridas
- TTR + historial básico en dashboard

### Fase 3 — Semántica avanzada

- Evaluación contextual (LLM)
- Anti-trampa
- Feedback empático avanzado

### Fase 4 — Voz y memoria

- ASR (Whisper o equivalente)
- Memoria semántica con pgvector

### Fase 5 — Analítica avanzada

- Densidad léxica y sofisticación
- Gráficas longitudinales

## Tecnologías detalladas

- Backend: Python 3.12, FastAPI, Uvicorn
- ORM/Migraciones: SQLAlchemy, Alembic
- NLP: spaCy para lematización
- LLM: OpenAI o Claude
- Colas: Celery
- Cache/Broker: Redis
- DB: PostgreSQL + pgvector
- Dashboard: Next.js + Tailwind + Recharts
- Infra: Docker, docker-compose

## Checklist open source

- LICENSE (Apache-2.0)
- README.md con quickstart
- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- .env.example (sin secretos)
- CI básico (lint + tests)

## Próximos pasos sugeridos

1) Definir `docker-compose.yml` y `docker-compose.prod.yml`
2) Diseñar esquema inicial de base de datos
3) Definir endpoints mínimos del MVP
4) Preparar documentación de setup local

## Estado actual (implementado)

- Scaffold mínimo en `apps/api`, `apps/worker`, `apps/scheduler`, `apps/dashboard`.
- `infra/compose/docker-compose.yml` y `infra/compose/docker-compose.prod.yml` listos.
- Base de datos inicial con SQLAlchemy + Alembic.
  - Modelos: `users`, `words`, `user_words`, `prompts`, `responses`, `streaks`, `ttr_metrics`.
  - Migración inicial: `apps/api/alembic/versions/0001_init_schema.py`.
- Documentación de setup local en `docs/setup-local.md`.
- Journey del usuario documentado en `docs/USER_JOURNEY.MD`.
- Guia de integracion WhatsApp en `docs/whatsapp.md`.
- Daily trigger en `apps/scheduler/src/scheduler.py`.
- Webhook y onboarding Telegram en `apps/api/src/routers/webhooks.py`.
- Guia de integracion Telegram en `docs/telegram.md`.
