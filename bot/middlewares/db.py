from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker


class DbMiddleware(BaseMiddleware):
    def __init__(self, db_session: async_sessionmaker):
        super().__init__()
        self.db_session = db_session

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.db_session() as session:
            data["session"] = session
            return await handler(event, data)


