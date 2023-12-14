import pytest
from bot.database import User, Address


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
