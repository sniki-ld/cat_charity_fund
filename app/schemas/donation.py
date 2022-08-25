# app/schemas/donation.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, NonNegativeInt, Extra


class DonationBase(BaseModel):
    """Базовый класс Pydantic-модели."""
    comment: Optional[str]
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'comment': 'С большим удовольствием!',
                'full_amount': 100
            }
        }


class DonationCreate(DonationBase):
    """Pydantic-модель для создания нового пожертвования."""
    pass


class DonationDB(DonationBase):
    """Pydantic-схема, для описания объекта, полученного из БД.
    для зарегистрированного пользователя.
    """
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationForSuperuserDB(DonationDB):
    """
    Pydantic-схема, для описания объекта, полученного из БД
    для суперюзера.
    """
    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: Optional[datetime]
