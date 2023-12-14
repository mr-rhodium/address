from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from bot.database.models.base import Base


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True,  autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Address {self.id}>"