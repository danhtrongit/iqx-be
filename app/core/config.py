from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "IQX API"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"
    POSTGRES_SCHEMA: str = "public"
    
    # TimescaleDB specific settings
    TIMESCALEDB_ENABLED: bool = True
    
    # SQLAlchemy connection string
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings() 