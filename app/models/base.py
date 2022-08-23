from sqlalchemy import Integer, Column, Boolean, DateTime
from datetime import datetime

from app.core.db import Base


class BaseModel(Base):
    """Базовая модель служит для определения базовых колонок в БД"""
    __abstract__ = True

    # требуемая сумма, целочисленное поле; больше 0;
    full_amount = Column(Integer)
    # внесённая сумма, целочисленное поле; значение по умолчанию — 0;
    invested_amount = Column(Integer, default=0)
    # булево значение, указывающее на то, собрана ли нужная сумма для проекта
    # (закрыт ли проект); значение по умолчанию — False;
    fully_invested = Column(Boolean, default=False)
    # дата создания проекта, тип DateTime, должно добавляться
    # автоматически в момент создания проекта.
    create_date = Column(DateTime, default=datetime.now)
    # дата закрытия проекта, DateTime, проставляется автоматически в
    # момент набора нужной суммы.
    close_date = Column(DateTime)