from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from bot.database.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,  autoincrement=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(32), unique=True, nullable=True)
    first_name = Column(String(32), nullable=True)
    last_name = Column(String(32), nullable=True)
    language = Column(String(2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relations
    addresses = relationship("Address", backref="users", lazy= "joined")

    def __repr__(self):
        return f"<User {self.id}>"