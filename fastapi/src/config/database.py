from typing import Optional

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class ConfigDatabase(BaseSettings):
    """Database configuration."""

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_NAME: str
    POSTGRES_ECHO: bool

    @property
    def database_url(self) -> Optional[PostgresDsn]:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"
        )

    class Config:
        env_file = "../pgsql/.env"
        env_file_encoding = 'utf-8'


settings_db = ConfigDatabase()
