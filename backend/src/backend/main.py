from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Field, Session, select
import uvicorn
from login import router as r_login
from models import Message

app = FastAPI()
app.include_router(r_login)

# creating database
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def chats_menu():
    return {"chats": "chats"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
