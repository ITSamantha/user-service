from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class AppConfig(BaseSettings):
    """Application configuration."""

    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"


settings_app = AppConfig()
