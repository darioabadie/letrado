# Letrado

Letrado es una plataforma SaaS B2C para ejercitar el vocabulario activo en hablantes nativos de espanol usando WhatsApp como canal principal y una capa de IA para evaluacion y feedback.

## Estructura del repositorio

```
/apps
  /api
    /src
    /tests
    Dockerfile
    pyproject.toml
  /worker
    /src
    /tests
    Dockerfile
    pyproject.toml
  /scheduler
    /src
    Dockerfile
    pyproject.toml
  /dashboard
    /src
    /public
    Dockerfile
    package.json

/infra
  /compose
    docker-compose.yml
    docker-compose.prod.yml

/docs
  plan-desarrollo.md
  architecture.md

/scripts
  migrate.sh
  seed.sh

/.github
  /workflows

LICENSE
README.md
CONTRIBUTING.md
CODE_OF_CONDUCT.md
.env.example
```

## Servicios y responsabilidades

### apps/api

Servicio principal FastAPI.

- Webhooks de WhatsApp (entrada y salida de mensajes).
- API REST para usuarios, vocabulario, prompts y metricas.
- Logica de negocio del MVP y orquestacion de tareas.

### apps/worker

Worker de Celery para tareas asincronas.

- Evaluacion semantica con LLM.
- Calculo de TTR y metricas derivadas.
- Generacion de feedback y tareas NLP.

### apps/scheduler

Programador de tareas (Celery beat).

- Envio de prompts diarios.
- Reintentos y tareas periodicas.

### apps/dashboard

Panel web (Next.js).

- Visualizacion de metricas (TTR, densidad, evolucion).
- Historial de conversaciones con resaltado.

### infra/compose

Definiciones de contenedores.

- `docker-compose.yml`: desarrollo local.
- `docker-compose.prod.yml`: parametros de produccion.

### docs

Documentacion del proyecto.

  - `plan-desarrollo.md`: roadmap tecnico y fases.
  - `architecture.md`: decisiones y arquitectura (por completar).
  - `api.md`: documentacion de endpoints y ejemplos.
  - `setup-local.md`: guia de setup local con Docker Compose.
  - `USER_JOURNEY.MD`: recorrido y casos de interaccion del usuario.
  - `whatsapp.md`: guia de integracion con WhatsApp Cloud API.

### scripts

Scripts operativos.

- Migraciones, seed inicial, tareas de bootstrap.

## Stack objetivo

- Backend: Python 3.12 + FastAPI
- Colas: Celery + Redis
- Base de datos: PostgreSQL + pgvector
- NLP: spaCy + LLM (OpenAI o Claude)
- Dashboard: Next.js
- Infra: Docker + docker-compose

## Notas

- Este repo es monorepo y todos los servicios corren en contenedores.
- La configuracion sensible vive en variables de entorno. Usar `.env.example` como referencia.

## Tests (API)

```bash
pip install -r apps/api/requirements.txt -r apps/api/requirements-dev.txt
pytest -c apps/api/pytest.ini
```
