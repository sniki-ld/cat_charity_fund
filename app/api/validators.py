from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    """Проверить название проекта на уникальность ."""
    charity_project = await charity_project_crud.get_charity_project_by_name(
        charity_project_name=charity_project_name,
        session=session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверить наличие проекта в БД по id."""
    charity_project = await charity_project_crud.get(
        obj_id=project_id,
        session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проекта с указанным id не существует!'
        )
    return charity_project


async def check_charity_project_before_edit(
        project_id: int,
        charity_project_in: CharityProjectUpdate,
        session: AsyncSession
) -> CharityProject:
    """Проверить проект перед редактированием."""
    charity_project = await check_charity_project_exists(
        project_id=project_id,
        session=session
    )
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )

    new_full_amount = charity_project_in.full_amount
    if (new_full_amount and
            charity_project.invested_amount > new_full_amount):
        raise HTTPException(
            status_code=400,
            detail='Нельзя установить требуемую сумму меньше уже вложенной'
        )

    new_name = charity_project_in.name
    await check_name_duplicate(
        charity_project_name=new_name,
        session=session
    )
    return charity_project


async def check_charity_project_before_delete(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверить проект перед удалением."""
    charity_project = await check_charity_project_exists(
        project_id=project_id,
        session=session
    )

    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )

    return charity_project
