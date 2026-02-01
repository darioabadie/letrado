from fastapi import FastAPI

from .routers.metrics import router as metrics_router
from .routers.prompts import router as prompts_router
from .routers.responses import router as responses_router
from .routers.users import router as users_router
from .routers.vocabulary import router as vocabulary_router
from .routers.webhooks import router as webhooks_router


app = FastAPI(title="Letrado API")

app.include_router(users_router)
app.include_router(vocabulary_router)
app.include_router(prompts_router)
app.include_router(responses_router)
app.include_router(metrics_router)
app.include_router(webhooks_router)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
