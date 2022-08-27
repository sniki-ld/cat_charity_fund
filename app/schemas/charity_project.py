# app/schemas/charity_project.py
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field, PositiveInt, NonNegativeInt, Extra


# class CharityProjectBase(BaseModel):
#     """Базовый класс Pydantic-модели."""
#
# name: Optional[str] = Field(None, min_length=1, max_length=100)
# description: Optional[str] = Field(None, min_length=1)
# full_amount: Optional[PositiveInt]

# class Config:
#     extra = Extra.forbid
#     schema_extra = {
#         'example': {
#             'name': 'Много вкусного',
#             'description': 'Средства для покупки корма',
#             'full_amount': 1000
#         }
#     }


class CharityProjectCreate(BaseModel):
    """Pydantic-модель для создания нового благотворительного проекта."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'Много вкусного',
                'description': 'Средства для покупки корма',
                'full_amount': 1000
            }
        }


class CharityProjectDB(CharityProjectCreate):
    """Pydantic-схема, для описания объекта, полученного из БД"""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(BaseModel):
    """Pydantic-модель для обновления благотворительного проекта."""
    name: Optional[str] = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'Много вкусного и интересного',
                'description': 'Средства для покупки корма и игрушек',
                'full_amount': 500
            }
        }
