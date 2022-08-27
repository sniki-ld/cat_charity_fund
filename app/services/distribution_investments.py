# 1. получаем все незакрытые проекты (unclosed projects)
# используем метод (get_not_closed_object) базового класса CRUDBase

# 2. получаем все незакрытые пожертвования (investments_open)
# используем метод (get_not_closed_object) базового класса CRUDBase

# 3. Распределяем свободные инвестиции:
# перебираем все пожертвования в цикле for и
# начиная с первого распределяем в открытые проекты (начиная с первого проекта в списке(перебираем в цикле for))

# 4. Присваиваем переменным к-во оставшихся после распределения средств:
# Для пожертвования:
# Сумма пожертвования "требуемая" (full_amount) минус сумма
# уже проинвестированная (invested_amount) =
# остаток средств после внесения (amount_of_available_donation)=>по сути это поле full_amount

# 5. То же делаем с проектами:
# требуемая сумма (full_amount) минус сумма
# уже проинвестированная (invested_amount) =
# сумма еще необходимая для проекта (amount_still_needed_for_project)=>по сути это поле full_amount

#  ЕСЛИ БЫ У НАС БЫЛ ТОЛЬКО ОДИН ПРОЕКТ И ТОЛЬКО ОДНО ПОЖЕРТВОВАНИЕ
#  ТО МЫ СДЕЛАЛИ БЫ ПРОВЕРКУ:
#  ОТНЯЛИ ОТ НУЖНОЙ ДЛЯ ПРОЕКТА СУММЫ СУММУ ИМЕЮЩЕГОСЯ ПОЖЕРТВОВАНИЯ
#  И ПО ПОЛУЧИВШЕЙСЯ РАЗНИЦЕ
#  (разница между требуемыми и инвестированными средствами)(difference_between_required_and_invested_funds)
#  ОПРЕДЕЛИЛИ БЫ ЧТО ДЕЛАТЬ С ОБЕКТАМИ (ПОЖЕРТВОВАНИЕМ И ПРОЕКТОМ):
#  ЕСЛИ РАЗНИЦА = 0 - ЗАКРЫВАЕМ ОБА ОБЪЕКТА
#  ЕСЛИ РАЗНИЦА < 0 - ЗАКРЫВАЕМ ПРОЕКТ, А ОСТАТОК СРЕДСТВ(РАЗНИЦА) ПОЖЕРТВОВАНИЯ ДОБАВЛЯЕМ (по модулю) В ПОЛЕ
#  внесённая сумма ПОЖЕРТВОВАНИЯ abs(invested_amount)и ЖДЕТ СЛЕД ОТКРЫТОГО ПРОЕКТА
#  ЕСЛИ РАЗНИЦА > 0 - ЗАКРЫВАЕМ ПОЖЕРТВОВАНИЕ, и увеличиваем собранную сумму проекта (invested_amount)
#  на сумму внесенных средств
#  (а ее мы получаем в переменной: остаток средств после внесения
#  (amount_of_available_donation)=>по сути это поле full_amount)
#  А ПРОЕКТ ЖДЕТ ПОПОЛНЕНИЯ  НУЖНОЙ СУММЫ

# теперь делаем все это в цикле

# НАПИШЕМ Ф-Ю закрывающую полностю проинвестированный объект
from datetime import datetime
from typing import Union

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation
from sqlalchemy.ext.asyncio import AsyncSession


def close_fully_invested_object(obj: Union[CharityProject, Donation]) -> None:
    # obj.fully_invested = (obj.fully_invested == obj.full_amount)
    # if obj.fully_invested:
    #     obj.close_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.now()


async def investment_process(session: AsyncSession):
    investments_open = await donation_crud.get_not_closed_object(
        session=session
    )
    unclosed_projects = await charity_project_crud.get_not_closed_object(
        session=session
    )
    if not investments_open or not unclosed_projects:
        return
    for donation in investments_open:
        for project in unclosed_projects:
            amount_still_needed_for_project = project.full_amount - project.invested_amount
            amount_of_available_donation = donation.full_amount - donation.invested_amount
            # разница между требуемыми и инвестированными средствами
            difference_between_required_and_invested_funds = amount_still_needed_for_project - amount_of_available_donation
            # ЕСЛИ РАЗНИЦА = 0 - ЗАКРЫВАЕМ ОБА ОБЪЕКТА
            if difference_between_required_and_invested_funds == 0:
                close_fully_invested_object(donation)
                close_fully_invested_object(project)
            # ЕСЛИ РАЗНИЦА < 0 - ЗАКРЫВАЕМ ПРОЕКТ, А ОСТАТОК СРЕДСТВ(РАЗНИЦА) ПОЖЕРТВОВАНИЯ ДОБАВЛЯЕМ
            # (по модулю) В ПОЛЕ внесённая сумма ПОЖЕРТВОВАНИЯ abs(invested_amount)
            if difference_between_required_and_invested_funds < 0:
                donation.invested_amount += abs(difference_between_required_and_invested_funds)
                close_fully_invested_object(project)
            # ЕСЛИ РАЗНИЦА > 0 - ЗАКРЫВАЕМ ПОЖЕРТВОВАНИЕ, и увеличиваем собранную сумму проекта (invested_amount)
            # на сумму внесенных средств
            if difference_between_required_and_invested_funds > 0:
                project.invested_amount += amount_of_available_donation
                close_fully_invested_object(donation)
        await session.commit()
