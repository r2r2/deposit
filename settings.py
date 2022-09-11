import os
from typing import Any

from core.config.config import config
from pydantic import BaseModel, BaseSettings, PostgresDsn, validator


DEBUG: bool = True


class UvicornConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000
    workers: int = os.cpu_count() if DEBUG is False else 2
    log_level: str = "info"


class Settings(BaseSettings):
    uvicorn_config: UvicornConfig = UvicornConfig()
    date_format: str = '%d.%m.%Y'
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True


settings = Settings(**config)
