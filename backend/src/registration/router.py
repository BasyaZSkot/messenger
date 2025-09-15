# from authlib.integrations.starlette_client import OAuth
from authx import AuthXConfig, AuthX
from fastapi import APIRouter, HTTPException, Depends, status, Request

from sqlalchemy.orm import Session
from starlette.responses import Response
from fastapi.responses import RedirectResponse

from .services import get_user, create_user
from .models import User, UserRegister, UserLogin
from src.db import get_db
from passlib.hash import sha256_crypt as crypt
import httpx
from google.oauth2 import id_token
from google.auth.transport import requests

GOOGLE_CLIENT_ID = "176267444936-hge2rci4g4ihtkkavluqq2vi41k9jlcp.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"

ALGORITHM = "HS256"
router = APIRouter()
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config)

@router.get("/google_login")
async def google_login(request: Request):
    redirect_uri = "http://localhost:8000/"#request.url_for('auth_callback')
    google_auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code&scope=openid email profile"

    return RedirectResponse(url=google_auth_url)

@router.get("/google_callback")
async def google_callback(code: str, request: Request):
    token_request_uri = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': request.url_for('auth_callback'),
        'grant_type': 'authorization_code',
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_request_uri, data=data)
        response.raise_for_status()
        token_response = response.json()

    id_token_value = token_response.get("id_token")
    if not id_token_value:
        raise HTTPException(status_code=400)

    try:
        id_info = id_token.verify_oauth2_token(id_token_value, requests.Request(), GOOGLE_CLIENT_ID)

        name = id_info.get('name')
        request.session['user_name'] = name

        return RedirectResponse(url=request.url_for('welcome'))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid id_token: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

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