from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as api_router
from app.api.web import router as web_router
from app.db import init_db
from app.logging_config import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    init_db()
    yield


app = FastAPI(title="Change Impact Mapper", version="0.1.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(Path(__file__).resolve().parent / "static")), name="static")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(web_router)
app.include_router(api_router)
