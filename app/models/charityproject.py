from sqlalchemy import Column, String, Text

from app.models.base import BaseModel


class CharityProject(BaseModel):
    """Модель для благотворительных проектов."""
    # уникальное название проекта, обязательное строковое поле;
    # допустимая длина строки — от 1 до 100 символов включительно;
    name = Column(String(100), unique=True, nullable=False)
    # описание, обязательное поле, текст; не менее одного символа;
    description = Column(Text, nullable=False)

