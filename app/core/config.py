from pathlib import Path
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    BOT_TOKEN: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / '.env'
    )


settings = Settings()
