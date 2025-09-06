from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


from ..db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, min_length=8)
    password = Column(String)
    is_superuser = Column(Boolean)

    # messages = relationship()
    # chats = relationship()

class UserRegister(BaseModel):
    username: str = Field()
    first_name: str = Field()
    last_name: str = Field()
    email: str = Field(examples=["...@gmail.com", "...@mail.ru"])
    password: str = Field(max_length=64, min_length=8)

class UserLogin(BaseModel):
    username: str = Field()
    email: str = Field(examples=["...@gmail.com", "...@mail.ru"])
    password: str = Field(max_length=64, min_length=8)
