from abc import ABC, abstractmethod
from typing import Callable

from sqlalchemy.sql.expression import select

from bot.database.models.address import Address
from bot.database.models.user import User


class AbstracDAO(ABC):
    @abstractmethod
    async def get(self, **kwargs):
        ...

    @abstractmethod
    async def create(self, **kwargs):
        ...

    @abstractmethod
    async def update(self, **kwargs):
        ...

    @abstractmethod
    async def delete(self, **kwargs):
        ...


class BaseDAO(AbstracDAO):
    def __init__(self, session):
        self.session = session

    async def get(self, model: Callable, id: int):
        return await self.session.get(model, id)

    async def create(self, model: Callable):
        self.session.add(model)
        await self.session.commit()
        return model

    async def update(self, model, **kwargs):
        for key, value in kwargs.items():
            setattr(model, key, value)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def delete(self, model):
        await self.session.delete(model)
        await self.session.commit()

    def get_or_create(self, **kwargs):
        user = self.session.query(self.model).filter_by(**kwargs).first()
        if not user:
            user = self.model(**kwargs)
            self.session.add(user)
            self.session.commit()
        return user


class UserDAO(BaseDAO):
    def __init__(self, session):
        self.session = session

    async def get_user(self, id: int) -> User:
        return await self.get(User, id)

    async def create_user(self, **kwargs) -> User:
        user = User(**kwargs)
        return await self.create(user)

    async def update_user(self, user: User, **kwargs):
        return await self.update(user, **kwargs)

    async def delete_user(self, user: User) -> None:
        await self.delete(user)

    async def one_user(self, **kwargs) -> User or None:
        statement = select(User).filter_by(**kwargs)
        out = await self.session.execute(statement)
        return out.unique().scalars().one_or_none()

    async def get_all_users(self) -> list[User]:
        statement = select(User)
        out = await self.session.execute(statement)
        return out.unique().scalars().all()

    async def filter_users(self, **kwargs) -> list[User]:
        statement = select(User).filter_by(**kwargs)
        out = await self.session.execute(statement)
        return out.unique().scalars().all()



class AddressDAO(BaseDAO):
    def __init__(self, session):
        self.session = session

    async def create(self, **kwargs) -> Address:
        address = Address(**kwargs)
        self.session.add(address)
        await self.session.commit()
        return address


