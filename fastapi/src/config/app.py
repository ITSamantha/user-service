from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class AppConfig(BaseSettings):
    """Application configuration."""

    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    UVICORN_APP_NAME: str
    UVICORN_HOST: str
    UVICORN_PORT: int
    UVICORN_RELOAD: bool

    class Config:
        env_file = "fastapi/.env"


settings_app = AppConfig()
