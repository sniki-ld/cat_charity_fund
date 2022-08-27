# app/schemas/donation.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Extra


class DonationCreate(BaseModel):
    """Pydantic-модель для создания нового пожертвования."""
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extras = Extra.forbid
        schema_extra = {
            'example': {
                'comment': 'Для котиков!',
                'full_amount': 50
            }
        }


# class DonationCreate(BaseModel):
#     """Pydantic-модель для создания нового пожертвования."""
#     pass

# class DonationDBUser(DonationCreate):
#     """Pydantic-схема, для описания объекта, полученного из БД.
#     для зарегистрированного пользователя.
#     """
#     id: int
#     create_date: datetime
#
#
#     class Config:
#         orm_mode = True

class DonationDB(DonationCreate):
    """Pydantic-схема, для описания объекта, полученного из БД.
    для зарегистрированного пользователя.
    """
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationAllDB(DonationDB):
    """
    Pydantic-схема, для описания объекта, полученного из БД
    для суперюзера.
    """
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]


# class DonationDBG(BaseModel):
#     """Pydantic-схема, для описания объекта, полученного из БД.
#     для зарегистрированного пользователя.
#     """
#     full_amount: PositiveInt
#     id: int
#     create_date: datetime
#
#     class Config:
#         orm_mode = True
