from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.config import config
from bot.database.models import MessageLink
from bot.database.core import async_session_maker

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Это поддержка HopJet.\n\n"
        "Напиши свой вопрос или расскажи, что не так, и мы ответим как можно скорее."
    )

@router.message(F.chat.type == "private")
async def handle_user_message(message: Message, bot: Bot):
    # Forward message to support group
    try:
        forwarded_msg = await message.forward(chat_id=config.SUPPORT_GROUP_ID)
        
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
        await message.answer("Произошла ошибка при отправке сообщения. Попробуйте позже.")
