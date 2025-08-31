from pydantic import BaseModel
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    name: str
    surname: str
    date_of_birth: datetime

class User(UserBase, talbe=True):
    id: int = Field(default=None, primary_key=True)

class MessageBase(SQLModel):
    text: str
    time: datetime
    user_from: User = Relationship()
    user_to: User = Relationship()

class Message(MessageBase, talbe=True):
    id: int = Field(default=None, primary_key=True)

