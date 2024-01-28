from functools import lru_cache

# from pydantic.env_settings import BaseSettings
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
