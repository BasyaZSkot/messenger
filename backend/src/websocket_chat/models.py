from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from src.db import Base


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

