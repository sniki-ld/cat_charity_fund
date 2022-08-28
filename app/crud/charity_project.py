from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession,
    ):
        """Вернуть проект по его названию."""
        db_charity_project = await session.execute(
            select(self.model).where(
                self.model.name == charity_project_name
            )
        )
        db_charity_project = db_charity_project.scalars().first()
        return db_charity_project


charity_project_crud = CRUDCharityProject(CharityProject)
