from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import Response

from .models import User, UserRegister
from sqlalchemy import or_, and_, select
from passlib.context import  CryptContext


myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])

async def get_user(db_session: Session, email: str, username: str)-> User | None:
        query = select(User).where(or_(User.email == email, User.username == username))
        user = db_session.execute(query).scalar_one_or_none()
        return user

async def create_user(db_session: Session, user_model) -> User:
    password = myctx.hash(user_model.password)
    new_user = User(email=user_model.email,
                    username=user_model.username,
                    password=password,
                    first_name=user_model.first_name,
                    last_name=user_model.last_name
                    )
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)

    return new_user





