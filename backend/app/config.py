from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "Urban City Analytics Backend"
    API_V1_STR: str = "/api"
    DEBUG: bool = True
    DATA_DIR: str = "data"
    UPLOAD_DIR: str = "uploads"
    PPLX_API_KEY: str | None = Field(default=None, env="PPLX_API_KEY")
    PPLX_BASE_URL: str = Field(default="https://api.perplexity.ai")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()
