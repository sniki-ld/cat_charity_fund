from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    """Базовый класс Pydantic-модели."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Pydantic-модель для создания нового благотворительного проекта."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        schema_extra = {
            'example': {
                'name': 'Много вкусного',
                'description': 'Средства для покупки корма',
                'full_amount': 1000
            }
        }


class CharityProjectDB(CharityProjectBase):
    """Pydantic-схема, для описания объекта, полученного из БД"""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    """Pydantic-модель для обновления благотворительного проекта."""
    pass
