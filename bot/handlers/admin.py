from aiogram import Router, F, Bot
from aiogram.types import Message
from sqlalchemy import select

from bot.config import config
from bot.database.models import MessageLink
from bot.database.core import async_session_maker

router = Router()

@router.message(F.chat.id == config.SUPPORT_GROUP_ID, F.reply_to_message)
async def handle_admin_reply(message: Message, bot: Bot):
    # Check if reply is to a forwarded message
    reply_to = message.reply_to_message
    if not reply_to:
        return

    async with async_session_maker() as session:
        # Find the original user
        stmt = select(MessageLink).where(MessageLink.support_message_id == reply_to.message_id)
        result = await session.execute(stmt)
        link = result.scalar_one_or_none()

        if link:
            try:
                # Send reply to user
                await bot.copy_message(
                    chat_id=link.user_chat_id,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id,
                    reply_to_message_id=link.user_message_id
                )
            except Exception as e:
                print(f"Error sending reply to user: {e}")
                await message.reply(f"Не удалось отправить сообщение пользователю: {e}")
        else:
            # Optionally notify that the user link was not found
            # await message.reply("Не удалось найти пользователя, связанного с этим сообщением.")
            pass
