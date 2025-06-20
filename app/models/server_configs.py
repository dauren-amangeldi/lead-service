from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, created_at, intpk, updated_at


class ServerConfigs(Base):
    __tablename__ = "server_configs"
    __table_args__ = {"schema": "public"}

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String)
    keyword: Mapped[str] = mapped_column(String)
    status_id: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]