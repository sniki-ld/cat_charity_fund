from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Проект пожертвования для котиков'
    description: str = 'API для Благотворительного фонда поддержки котиков'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'

    class Config:
        env_file = '.env'


settings = Settings()
