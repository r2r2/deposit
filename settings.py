import os

from pydantic import BaseModel, BaseSettings


class UvicornConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000
    workers: int = os.cpu_count()
    log_level: str = "info"


class Settings(BaseSettings):
    uvicorn_config: UvicornConfig = UvicornConfig()
    date_format: str = '%d.%m.%Y'
