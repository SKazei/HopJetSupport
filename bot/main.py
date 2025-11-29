import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import config
from bot.handlers import user, admin
from bot.database.core import init_db

async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Initialize DB
    await init_db()
    
    bot = Bot(token=config.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()
    
    dp.include_router(user.router)
    dp.include_router(admin.router)
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
