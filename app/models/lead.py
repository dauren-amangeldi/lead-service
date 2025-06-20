from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, created_at, intpk, updated_at


class Lead(Base):
    __tablename__ = "leads"
    __table_args__ = {"schema": "public"}

    id: Mapped[intpk]
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    phonecc: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    user_ip: Mapped[str] = mapped_column(String)
    aff_sub: Mapped[str] = mapped_column(String)
    aff_sub2: Mapped[str] = mapped_column(String)
    aff_sub3: Mapped[str] = mapped_column(String)
    aff_sub4: Mapped[str] = mapped_column(String)
    aff_id: Mapped[str] = mapped_column(String)
    offer_id: Mapped[str] = mapped_column(String)
    status_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at] 