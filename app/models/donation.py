from sqlalchemy import Column, Text, Integer, ForeignKey

from app.models.base import BaseModel


class Donation(BaseModel):
    """Модель для пожертвований."""
    # id пользователя, сделавшего пожертвование.
    # Foreign Key на поле user.id из таблицы пользователей;
    # У внешнего ключа должно быть имя.
    user_id = Column(Integer, ForeignKey('user.id', name='fk_donation_user_id_user'))
    # необязательное текстовое поле;
    # Значение nullable по умолчанию равно True, поэтому его можно не указывать.
    comment = Column(Text)