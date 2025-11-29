from datetime import datetime
from sqlalchemy import BigInteger, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from bot.models.base import Base

class MessageLink(Base):
    __tablename__ = "message_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    support_message_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    user_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_message_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
