from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Проект пожертвования для котиков'
    description: str = 'API для Благотворительного фонда поддержки котиков'

    class Config:
        env_file = '.env'


settings = Settings()
