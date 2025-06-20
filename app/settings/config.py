import os
import pathlib
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import AnyHttpUrl

load_dotenv()

class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    # SECURITY_BCRYPT_ROUNDS: int = 12
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520  # 8 days
    # REFRESH_TOKEN_EXPIRE_MINUTES: int = 40320  # 28 days
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1", "0.0.0.0", "*"]

    PROJECT_NAME: str = "Lead Redirect Service"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Lead Redirect Service"
    WWW_DOMAIN = ""
    
    DATABASE_USER: str = os.getenv("POSTGRES_USER")  # type: ignore # ignored because we get it from env
    DATABASE_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")  # type: ignore # ignored because we get it from env
    DATABASE_HOST: str = "db"  # Use service name for container-to-container communication
    DATABASE_NAME: str = os.getenv("POSTGRES_DB")  # type: ignore # ignored because we get it from env
    DATABASE_PORT: str = "5432"  # Use internal PostgreSQL port for container communication
    DATABASE_URL: str = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

class DevelopmentConfig(BaseConfig):
    config_name = os.environ.get("FASTAPI_CONFIG", "DEV")  # type: ignore # ignored because we get it from env
    TELEGRAM_API = os.getenv("TELEGRAM_API")  # type: ignore # ignored because we get it from env
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # type: ignore # ignored because we get it from env

class ProductionConfig(BaseConfig):
    config_name = os.environ.get("FASTAPI_CONFIG", "PROD")  # type: ignore # ignored because we get it from env
    TELEGRAM_API = os.getenv("TELEGRAM_API")  # type: ignore # ignored because we get it from env
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # type: ignore # ignored because we get it from env

class TestingConfig(BaseConfig):
    config_name = os.environ.get("FASTAPI_CONFIG", "TEST")  # type: ignore # ignored because we get it from env
    TELEGRAM_API = os.getenv("TELEGRAM_API")  # type: ignore # ignored because we get it from env
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # type: ignore # ignored because we get it from env
class LocalConfig(BaseConfig):
    config_name = os.environ.get("FASTAPI_CONFIG", "LOCAL")  # type: ignore # ignored because we get it from env
    TELEGRAM_API = os.getenv("TELEGRAM_API")  # type: ignore # ignored because we get it from env
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # type: ignore # ignored because we get it from env

@lru_cache
def get_settings():
    config_cls_dict = {
        "DEV": DevelopmentConfig,
        "PROD": ProductionConfig,
        "TEST": TestingConfig,
        "LOCAL": LocalConfig,
    }

    config_name = os.environ.get("FASTAPI_CONFIG", "DEV")
    config_cls = config_cls_dict[config_name]
    return config_cls()

settings = get_settings()
