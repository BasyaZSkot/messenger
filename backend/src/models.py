from typing import Optional

from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey
from db import Base

# class UserBase(SQLModel):
#     name: str
#     surname: str
#     date_of_birth: datetime
#
# class User(UserBase, table=True):
#     __table_name__ = "User"
#     id: int = Field(default=None, primary_key=True)

class MessageCreate(BaseModel):
    text: str
    user_to: str
    user_from: str
    created_at: datetime

    class Config:
        orm_mode = True

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    user_to = Column(String)
    user_from = Column(String)
    created_at = Column(DateTime, default=datetime.now)


