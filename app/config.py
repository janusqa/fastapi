from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    api_server: str
    api_port: int
    api_debug: bool
    api_log: bool
    db_server: str
    db_port: int
    db_uid: str
    db_pid: str
    db_name: str
    oauth2_secret_key: str
    oauth2_algorithm: str
    oauth2_expire_min: int

    class Config:
        env_file = "app/.env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()
