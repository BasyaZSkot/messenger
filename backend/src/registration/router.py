from authx import AuthXConfig, AuthX
from fastapi import APIRouter, HTTPException, Depends, status

from sqlalchemy.orm import Session
from starlette.responses import Response

from .services import get_user, create_user
from .models import User, UserRegister, UserLogin
from src.db import get_db
from passlib.hash import sha256_crypt as crypt



router = APIRouter()
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config)

@router.post("/registration/")
async def registration(model: UserRegister, response: Response, session: Session = Depends(get_db)):
    if await get_user(session, model.email, model.username ):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    try:
        user: User = await create_user(session, model)
        token = security.create_access_token(uid=str(user.id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, value=token)
        return {"token": token}
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/login/")
async def login(login_model: UserLogin, response: Response, db_session: Session = Depends(get_db)):
    user = await get_user(db_session, login_model.email, login_model.username)
    if not crypt.verify(login_model.password, user.password, ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=user.email)
    token = security.create_access_token(uid=str(user.id))
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, value=token)
    return {"access_token": token}