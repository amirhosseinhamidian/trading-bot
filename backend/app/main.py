from fastapi import FastAPI

from app.core.config import settings
from app.api.v1 import routes_health, routes_signals
from app.db.session import Base, engine

from app.db import models  # noqa: F401


app = FastAPI(title=settings.PROJECT_NAME)


@app.on_event("startup")
def on_startup() -> None:
    # وقتی اینجا می‌رسه، چون models import شده،
    # Base.metadata الان همه‌ی таблиهارو می‌شناسه
    Base.metadata.create_all(bind=engine)


app.include_router(
    routes_health.router,
    prefix=settings.API_V1_PREFIX,
    tags=["health"],
)

app.include_router(
    routes_signals.router,
    prefix=settings.API_V1_PREFIX,
    tags=["signals"],
)
