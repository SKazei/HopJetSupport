import asyncio
from bot.database.core import init_db, engine
from bot.database.models import MessageLink
from sqlalchemy import select
from bot.database.core import async_session_maker

async def check_db():
    print("Initializing database...")
    await init_db()
    print("Database initialized.")
    
    print("Checking session...")
    async with async_session_maker() as session:
        # Try a simple query
        stmt = select(MessageLink).limit(1)
        await session.execute(stmt)
        print("Session check passed.")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_db())
