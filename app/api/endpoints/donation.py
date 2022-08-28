from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationAllDB, DonationCreate, DonationDB
from app.services.distribution_investments import investment_process
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


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
        user: User = Depends(current_user)
):
    """
    Вернуть список всех пожертвований текущего пользователя.
    Только для авторизованных пользователей.
    """
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
