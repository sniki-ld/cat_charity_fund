# app/core/base.py
"""Импорты класса Base и всех моделей для Alembic."""
# Чтобы IDE не ругалась на неиспользуемые импорты, напротив каждой строки
# поставьте inline-комментарий со специальным обозначением noqa
# (_NO Quality Assurance_: «Без обеспечения качества»):
from app.core.db import Base  # noqa
from app.models import CharityProject, Donation, User  # noqa
