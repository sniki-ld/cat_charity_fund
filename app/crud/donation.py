"""Использование класса CRUDBase в проекте"""
# Теперь мы для любой новой модели можем сразу подключить пять CRUD-методов,
# создав объект класса CRUDBase и передав в него нужную модель.
from datetime import datetime

from sqlalchemy import select, and_, or_, between
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    async def get_my_donations(
            self, session: AsyncSession, user: User
    ) -> List[Donation]:
        """
        Метод, позволяющий зарегистрированным пользователям
        получить список своих пожертвований.
        """
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
