from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
print(BASE_DIR)


class Settings(BaseSettings):
    db_url: str
    session_key: str
    max_message_size: int = 51200  # 50 KB
    max_storage_bytes: int = 2147483648  # 2 GB

    class Config:
        env_file = ".env"


settings = Settings()
