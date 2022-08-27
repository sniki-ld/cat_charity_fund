from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate, DonationDB, DonationAllDB
# Добавьте импорт зависимости, определяющей,
# что текущий пользователь - суперюзер.
from app.core.user import current_user, current_superuser
from app.models import User
from app.services.distribution_investments import investment_process

router = APIRouter()


#
# """Получение объекта пользователя в запросе
# Чтобы сохранить id текущего пользователя в столбце с внешним ключом,
# нужно получить объект пользователя из запроса. Для этого используется система DI."""
#  в параметры эндпоинта мы добавили зависимость с пользователем (DI)

# Если необходимо ограничить доступ для неавторизованных пользователей к
# определённому эндпоинту, но при этом объект пользователя не требуется передавать
# в функцию, обрабатывающую запрос — класс Depends следует указать не в
# параметрах функции, а в декораторе эндпоинта, в параметре dependencies.
# Этот параметр принимает список объектов, даже если передан всего один элемент.
# Добавим параметр dependencies=[Depends(current_superuser)] к запросу на
# получение списока всех бронирований:


@router.get(
    '/',
    response_model=list[DonationAllDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Вернуть список всех пожертвований.
    Только для суперюзеров.
    """
    return await donation_crud.get_multi(session=session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        # В этой зависимости получаем обычного пользователя, а не суперюзера.
        user: User = Depends(current_user)
):
    """
    Получить список всех пожертвований для текущего пользователя.
    Только для авторизованных пользователей.
    """
    # Вызываем созданный метод.
    return await donation_crud.get_my_donations(
        session=session, user=user
    )


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
        donation_in: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """
    Создать новое пожертвование.
    Только для авторизированного пользователя.
    """
    new_donation = await donation_crud.create(
        obj_in=donation_in, session=session, user=user
    )
    await investment_process(session=session)
    await session.refresh(new_donation)
    return new_donation
