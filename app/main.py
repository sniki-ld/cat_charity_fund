from fastapi import FastAPI
from app.core.config import settings
from app.core.init_db import create_first_superuser

app = FastAPI(
    title=settings.app_title,
    description=settings.description
)


@app.on_event('startup')
async def startup():
    """При старте приложения запускаем корутину create_first_superuser."""
    await create_first_superuser()