from fastapi import FastAPI
from app.routers import links

app = FastAPI()
app.include_router(links.router)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
