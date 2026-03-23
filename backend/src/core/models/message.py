from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_path: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    message_hash: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    message_salt: Mapped[str] = mapped_column(String(100), nullable=False)
