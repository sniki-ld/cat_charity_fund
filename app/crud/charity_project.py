# app/crud/charity_project.py
from app.models.charity_project import CharityProject

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Возвращает id проекта по его названию."""
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        db_charity_project_id = db_charity_project_id.scalars().first()
        return db_charity_project_id


charity_project_crud = CRUDCharityProject(CharityProject)
