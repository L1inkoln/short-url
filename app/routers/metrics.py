from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from fastapi import APIRouter

router = APIRouter(tags=["metrics"])


# Prometheus
@router.get("/metrics")
@router.get("/metrics/")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
