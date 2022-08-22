from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """Основа для базового класса моделей."""
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


# В качестве основы для базового класса укажем класс PreBase.
Base = declarative_base(cls=PreBase)  # базовый класс для будущих моделей

engine = create_async_engine(settings.database_url)  # создайте движок

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)  # множественно создавать сессии


async def get_async_session():
    """Асинхронный генератор сессий."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
