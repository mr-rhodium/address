import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.database import Base

engine = create_async_engine(
    "sqlite+aiosqlite:///test_db.sqlite3", echo=False, future=True
)


@pytest.fixture()
def user_data():
    return {
        "tg_id": 1,
        "username": "test_user",
        "first_name": "test",
        "last_name": "user",
        "language": "en",
    }


@pytest.fixture()
def user_data_two():
    return {
        "tg_id": 2,
        "username": "test_user_two",
        "first_name": "test_two",
        "last_name": "user_two",
        "language": "en",
    }


@pytest.fixture()
def address_data():
    return {"user_id": 1, "address": "London, England, zipcode: 123456"}


@pytest.fixture(name="session")
async def session_fixture():
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    async with sessionmaker() as s:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield s

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
