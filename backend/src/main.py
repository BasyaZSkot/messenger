from fastapi import FastAPI, Depends, Request
import uvicorn
from registration.router import router as registration_r
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
import models as md
from db import get_db


app = FastAPI()
app.include_router(registration_r)
templates = Jinja2Templates(directory="src/static/")

@app.get("/")
async def chats_menu(request: Request):
    return templates.TemplateResponse("/login.html", {"request": request})


@app.get("/chat123412", )
async def chat(session: Session = Depends(get_db)):
    messages = session.query(md.Message).all()
    return messages
@app.post("/chat123412")
async def chat_send(
        message: md.MessageCreate,
        session: Session = Depends(get_db)
):
    new_message = md.Message(text=message.text, user_from=message.user_from, user_to=message.user_to, created_at=message.created_at)
    session.add(new_message)
    session.commit()
    session.refresh(new_message)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, )
