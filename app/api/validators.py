# app/api/validators.py
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    """Проверить наличие дубликата названия проекта."""
    charity_project_id = await charity_project_crud.get_charity_project_id_by_name(
        charity_project_name=charity_project_name, session=session)
    if charity_project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверить наличие проекта в БД по id."""
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_before_edit(
        charity_project_id: int,
        odj_in: CharityProjectUpdate,
        session: AsyncSession
) -> CharityProject:
    """
    Проверить перед редактированием проекта:
        - наличие в БД;
        - наличие дубликата названия проекта;
        - проект не должен быть закрыт;
        - новая сумма требуемых инвестиций (odj_in.full_amount)
        не должна быть меньше уже имеющейся (charity_project.invested_amount);
    """

    charity_project = await check_charity_project_exists(
        charity_project_id=charity_project_id, session=session
    )
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )

    await check_name_duplicate(charity_project_name=charity_project.name, session=session)

    if odj_in.full_amount and odj_in.full_amount < charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Нельзя установить требуемую сумму меньше уже вложенной'
        )
    return charity_project


async def check_charity_project_before_delete(
        charity_project_id: int,
        session: AsyncSession
) -> CharityProject:
    """
    Проверить перед удалением проекта:
        - наличие в БД;
        - были ли инвестированы средства;
    """
    charity_project = await check_charity_project_exists(
        charity_project_id=charity_project_id, session=session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity_project
