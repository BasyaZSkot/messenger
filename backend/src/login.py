from fastapi import APIRouter, HTTPException
from authx import AuthX, AuthXConfig
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.responses import Response

router = APIRouter()
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

class UserLoginShema(BaseModel):
    username: str
    password: str


@router.post('/login')
async def login(creds: UserLoginShema, response: Response):
    if creds.username == "test" and creds.password == "test":
        token = security.create_access_token(uid="1234")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, value=token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@router.get('/protected', dependencies=[Depends(security.access_token_required)])
async def protected():
    return {"data": "top_secret"}

@router.get('/logout', dependencies=[Depends(security.access_token_required)])
def logout(response:Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)