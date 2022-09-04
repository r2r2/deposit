import os
from pydantic import BaseSettings, BaseModel


class UvicornConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000
    # "workers": int = os.cpu_count()
    workers: int = 2
    log_level: str = "info"


class Settings(BaseSettings):
    uvicorn_config: UvicornConfig = UvicornConfig()
