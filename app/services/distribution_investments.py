from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


def close_fully_invested_object(obj: Union[CharityProject, Donation]) -> None:
    """Закрыть объект c полностью распределёнными инвестициями."""
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.now()


async def investment_process(session: AsyncSession):
    """
    Процесс инвестирования:распределить доступную сумму пожертвования
    по открытым проектам.
    """
    investments_open = await donation_crud.get_not_closed_objects(
        session=session
    )
    unclosed_projects = await charity_project_crud.get_not_closed_objects(
        session=session
    )
    if not investments_open or not unclosed_projects:
        return
    for donation in investments_open:
        for project in unclosed_projects:
            amount_still_needed_for_project = (
                project.full_amount - project.invested_amount)
            amount_of_available_donation = donation.full_amount - donation.invested_amount
            difference_between_required_and_invested_funds = (
                amount_still_needed_for_project - amount_of_available_donation)

            if difference_between_required_and_invested_funds == 0:
                close_fully_invested_object(donation)
                close_fully_invested_object(project)

            if difference_between_required_and_invested_funds < 0:
                donation.invested_amount += abs(difference_between_required_and_invested_funds)
                close_fully_invested_object(project)

            if difference_between_required_and_invested_funds > 0:
                project.invested_amount += amount_of_available_donation
                close_fully_invested_object(donation)
        await session.commit()
