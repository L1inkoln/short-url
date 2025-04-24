import logging
from fastapi import FastAPI
from app.routers import links, metrics


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(links.router)
app.include_router(metrics.router)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
