from authx import AuthXConfig, AuthX
from fastapi import APIRouter, HTTPException, Depends, status

from sqlalchemy.orm import Session
from starlette.responses import Response

from .services import get_user, create_user
from .models import User, UserRegister
from ..main import get_db
from passlib.context import  CryptContext


myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])

router = APIRouter()
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config)

@router.post("/registration/")
async def registration(session: Session = Depends(get_db), model=UserRegister) -> User|HTTPException|None:
    if await get_user(session, model.email, model.username ):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    try:
        user: User = await create_user(session, model)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    return user

@router.post("/login/")
async def login(db_session: Session, login_model, response: Response):
    user = await get_user(db_session, login_model.email, login_model.username)
    if user.password != myctx.hash(login_model.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    token = await create_access_token(uid=user.id)
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, value=token)
    return {"access_token": token}