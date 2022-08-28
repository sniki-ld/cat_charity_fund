from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    async def get_my_donations(
            self,
            session: AsyncSession,
            user: User
    ):
        """
        Получить список своих пожертвований.
        Только для зарегистрированных пользователей.
        """
        donations = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
