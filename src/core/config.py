from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
print(BASE_DIR)


class Settings(BaseSettings):
    db_url: str
    session_key: str

    class Config:
        env_file = ".env"


settings = Settings()
