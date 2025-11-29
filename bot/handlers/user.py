from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.config import config
from bot.models.models import MessageLink
from bot.database.core import async_session_maker
from bot.i18n import t
from bot.services.UserService import UserService

router = Router()
user_service = UserService()

@router.message(CommandStart())
async def cmd_start(message: Message):
    try:
        user = await user_service.get_current_user(message.from_user.id)
        lang = user_service.get_user_preferred_language(user, message.from_user)
        await message.answer(t("start.greeting", lang))
    except Exception as e:
        print(e)


@router.message(F.chat.type == "private")
async def handle_user_message(message: Message, bot: Bot):
    # Forward message to support group
    try:
        lang = await user_service.get_user_language(message.from_user.id)
        forwarded_msg = await message.forward(chat_id=config.SUPPORT_GROUP_ID)
        await message.answer(t("start.common.message", lang))
        
        # Save link to DB
        async with async_session_maker() as session:
            link = MessageLink(
                support_message_id=forwarded_msg.message_id,
                user_chat_id=message.chat.id,
                user_message_id=message.message_id
            )
            session.add(link)
            await session.commit()
            
    except Exception as e:
        print(f"Error forwarding message: {e}")
        await message.answer("Error.")
