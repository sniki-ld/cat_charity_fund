from app.api.validators import (check_charity_project_before_delete,
                                check_charity_project_before_edit,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.distribution_investments import investment_process
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Создать новый благотворительный проект.
    Только для суперпользователей.
    """
    await check_name_duplicate(
        charity_project_name=charity_project.name,
        session=session
    )
    new_charity_project = await charity_project_crud.create(
        obj_in=charity_project,
        session=session
    )
    await investment_process(session=session)
    await session.refresh(new_charity_project)

    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Получить список всех благотворительных проектов.
    Доступно любому пользователю.
    """
    return await charity_project_crud.get_multi(session=session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
        project_id: int,
        charity_project_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Редактировать благотворительный проект.
    Закрытый проект нельзя редактировать.
    Требуемая сумма должна быть больше уже внесенной.
    Только для суперюзеров.
    """
    charity_project_db = await check_charity_project_before_edit(
        project_id=project_id,
        charity_project_in=charity_project_in,
        session=session
    )

    charity_project = await charity_project_crud.update(
        db_obj=charity_project_db,
        obj_in=charity_project_in,
        session=session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Удалить благотворительный проект.
    Нельзя удалить можно, только закрыть, если в проект
    уже были внесены средства.
    Только для суперюзеров.
    """
    charity_project = await check_charity_project_before_delete(
        project_id=project_id,
        session=session
    )

    charity_project = await charity_project_crud.delete(
        db_obj=charity_project,
        session=session
    )
    return charity_project
