import pytest
from bot.database import User, Address
from bot.database.dao import UserDAO


@pytest.mark.asyncio
async def test_user_model(session, user_data):
    user = User(**user_data)
    session.add(user)
    await session.commit()
    assert user.id == 1
    assert user.tg_id == 1
    assert user.username == "test_user"
    assert user.first_name == "test"
    assert user.last_name == "user"
    assert user.language == "en"

@pytest.mark.asyncio
async def test_address_model(session, user_data, address_data):

    user = User(**user_data)
    session.add(user)
    await session.commit()
    address = Address(**address_data)
    session.add(address)
    await session.commit()
    assert address.id == 1
    assert address.user_id == 1
    assert address.address == address_data["address"]
    await session.refresh(user)

    assert user.addresses == [address]

@pytest.mark.asyncio
async def test_dao_create_user(session, user_data):
    user = await UserDAO(session).create_user(**user_data)

    assert user.id == 1
    assert user.tg_id == 1
    assert user.username == "test_user"
    assert user.first_name == "test"
    assert user.last_name == "user"
    assert user.language == "en"

async def test_dao_get_user(session, user_data):
    user = await UserDAO(session).create_user(**user_data)

    found_user = await UserDAO(session).get_user(user.id)

    assert found_user.id == 1
    assert found_user.tg_id == 1
    assert found_user.username == "test_user"
    assert found_user.first_name == "test"
    assert found_user.last_name == "user"
    assert found_user.language == "en"

async def test_dao_update_user(session, user_data):
    user = await UserDAO(session).create_user(**user_data)
    updated_user = await UserDAO(session).update_user(user, username="updated_username")

    assert updated_user.id == 1
    assert updated_user.tg_id == 1
    assert updated_user.username == "updated_username"
    assert updated_user.first_name == "test"
    assert updated_user.last_name == "user"
    assert updated_user.language == "en"

async def test_dao_delete_user(session, user_data):
    user = await UserDAO(session).create_user(**user_data)
    await UserDAO(session).delete_user(user)
    found_user = await UserDAO(session).get_user(user.id)
    assert found_user is None

async def test_get_all_users(session, user_data, user_data_two):
    user = await UserDAO(session).create_user(**user_data)
    user_two = await UserDAO(session).create_user(**user_data_two)
    users = await UserDAO(session).get_all_users()

    assert len(users) == 2
    assert users[0].id == 1
    assert users[0].tg_id == 1
    assert users[0].username == "test_user"
    assert users[0].first_name == "test"
    assert users[0].last_name == "user"
    assert users[0].language == "en"

    assert users[1].id == 2
    assert users[1].tg_id == 2
    assert users[1].username == "test_user_two"
    assert users[1].first_name == "test_two"
    assert users[1].last_name == "user_two"

async def test_filter(session, user_data):
    user = await UserDAO(session).create_user(**user_data)
    users = await UserDAO(session).filter_users(username="test_user")

    assert users[0].id == user.id
async def test_first_user(session, user_data):

    user = await UserDAO(session).create_user(**user_data)
    one_user = await UserDAO(session).one_user(username="test_user")

    assert one_user.id == user.id

  