from aiogram.types import Message

from bot.database.dao import AddressDAO, UserDAO


class Error:
    id: str = "Wrong ID"


class Formatter:
    def __init__(self, data):
        self.data = data

    async def count(self):
        return len(self.data.addresses)

    async def address_text(self):
        if self.data.addresses:
            return " \n".join([item.address for item in self.data.addresses])
        return "User has no addresses"

    async def formatted(self):
        if self.data:
            count = await self.count()
            addresses = await self.address_text()
            return f"Count addresses: {count}\n Addresses: \n{addresses}"
        return "User not found"


class GeneralLogic:
    def __init__(self, sessiin) -> None:
        self.session = sessiin

    async def add_user(self, message: Message):
        result = await UserDAO(self.session).one_user(tg_id=message.from_user.id)
        if not result:
            return await UserDAO(self.session).create_user(
                tg_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                language=message.from_user.language_code,
            )

    async def info(self, id: str):
        if id.isdigit():
            user_data = await UserDAO(self.session).one_user(tg_id=id)
            return await Formatter(user_data).formatted()
        return Error.id

    async def add_address(self, message: Message):
        user = await UserDAO(self.session).one_user(tg_id=message.from_user.id)
        return await AddressDAO(self.session).create(
            user_id=user.id, address=message.text
        )
