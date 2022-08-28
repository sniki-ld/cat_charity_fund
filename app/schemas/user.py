from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема с базовыми полями модели пользователя (кроме пароля)."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """
    Схема для создания пользователя;
    в неё обязательно должны быть переданы email и password.
    """
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """
    Схема для обновления объекта пользователя;
    содержит все базовые поля модели пользователя (в том числе и пароль).
    """
    pass
