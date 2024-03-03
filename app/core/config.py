from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / '.env'
    )


settings = Settings()


# def create_async_db_engine():
#     engine = create_async_engine(settings.DATABASE_URL, echo=True)
#     return engine
