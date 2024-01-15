from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import users
from db.mongodb import MongoDB
import uvicorn
import os


MONGO_URI = os.environ['APP_URI']


@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDB.connect_to_db(MONGO_URI)
    yield
    await MongoDB.close_db_connection()

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# TODO: Add a way to add channels to a user
# TODO: Add channels and messages endpoints
