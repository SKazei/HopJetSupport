import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv

# Load .env manually to ensure we can run this standalone
load_dotenv()

async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Error: BOT_TOKEN not found in .env file.")
        print("Please create .env file and add BOT_TOKEN=your_token_here")
        return

    bot = Bot(token=token)
    dp = Dispatcher()

    print("Bot started. Add the bot to your group and send a message there.")
    print("Waiting for messages...")

    @dp.message()
    async def handler(message: Message):
        print(f"Received message in chat: {message.chat.title} (ID: {message.chat.id})")
        print(f"Chat Type: {message.chat.type}")
        print("-" * 20)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
