import asyncio
from aiogram import Bot, Dispatcher
from bot.middlewares.db import DbMiddleware

from bot.handlers import commands
# sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.config import conf
async def main():
    # db connetion
    engine = create_async_engine(conf.database_url, echo=False, future=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    # Bot
    bot  = Bot(token=conf.bot_token.get_secret_value(), parse_mode="HTML")
    # Dispatcher
    dp = Dispatcher()
    
    # middlewares
    dp.update.middleware(DbMiddleware(db_session=sessionmaker))

    # Register handlers
    dp.include_router(commands.router)


    # Start long-polling
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())