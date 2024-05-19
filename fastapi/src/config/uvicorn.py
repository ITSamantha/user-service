from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class UvicornConfig(BaseSettings):
    """Application configuration."""

    UVICORN_APP_NAME: str
    UVICORN_HOST: str
    UVICORN_PORT: int
    UVICORN_RELOAD: bool

    class Config:
        env_file = "fastapi/.env"
        env_file_encoding = 'utf-8'
        extra = "ignore"


settings_uvicorn = UvicornConfig()
