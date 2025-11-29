import logging
from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from bot.database.core import get_session
from bot.models.user import User
from bot.i18n.locales import LANGUAGES



class UserService:

    async def get_current_user(self, user_telegram_id: int) -> Optional[User]:
        """
        Получает текущего пользователя по telegram_id
        """
        async with get_session() as session:
            try:
                result = await session.execute(
                    select(User).where(User.user_id == user_telegram_id)
                )
                user = result.scalar_one_or_none()
                return user
            except SQLAlchemyError as e:
                raise Exception(f"Database error getting user: {e}")

    async def get_user_language(self, user_telegram_id: int) -> str:
        """
        Получает язык пользователя
        """
        user = await self.get_current_user(user_telegram_id)
        return getattr(user, "language", "en") if user else "en"

    def get_user_preferred_language(self, user: Optional[User], telegram_user) -> str:
        """
        Получает предпочтительный язык пользователя
        """
        if user is None:
            return self.get_user_language_from_telegram(telegram_user)
        else:
            return user.language or "en"
    def get_user_language_from_telegram(self, telegram_user) -> str:
        """
        Получает язык пользователя из Telegram профиля
        """
        lang = (telegram_user.language_code or "en").split("-")[0].lower()
        if lang not in LANGUAGES:
            lang = "en"  # fallback, если язык не поддерживается
        return lang