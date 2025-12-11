# bot/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime, func
from bot.models.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)   # internal DB id
    user_id = Column(BigInteger, unique=True, nullable=False)  # telegram chat_id / user.id
    language = Column(String(8))
    currency = Column(String(8))
    usFormat = Column(Boolean, default=False, nullable=True)
    location = Column(String(8))
    first_name = Column(String(64), nullable=True)
    last_name = Column(String(64), nullable=True)
    registered_at = Column(DateTime, server_default=func.now(), nullable=True)
    last_seen = Column(DateTime, nullable=True)
    source = Column(String(64), nullable=True)