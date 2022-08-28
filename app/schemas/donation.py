from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


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
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
