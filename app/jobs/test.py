import os
import pathlib
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import AnyHttpUrl

load_dotenv()

DATABASE_USER: str = os.getenv("POSTGRES_USER")  # type: ignore # ignored because we get it from env
DATABASE_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")  # type: ignore # ignored because we get it from env
DATABASE_HOST: str = "db"  # Use service name for container-to-container communication
DATABASE_NAME: str = os.getenv("POSTGRES_DB")  # type: ignore # ignored because we get it from env
DATABASE_PORT: str = "5432"  # Use internal PostgreSQL port for container communication
DATABASE_URL: str = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

print(DATABASE_URL)
