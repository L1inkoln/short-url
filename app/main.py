import logging
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.routers import links, metrics


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(links.router)
app.include_router(metrics.router)
Instrumentator().instrument(app).expose(app)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
