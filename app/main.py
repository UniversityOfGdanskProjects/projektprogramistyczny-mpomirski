from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import users, channels, messages, calls, screenshares, files, notifications, auth
from db.mongodb import MongoDB
import uvicorn
import os

MONGO_URI = os.environ['DATABASE_URI']


@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDB.connect_to_db(MONGO_URI)
    yield
    await MongoDB.close_db_connection()

app = FastAPI(lifespan=lifespan, root_path='/app/2')
routers = [users, channels, messages, calls,
           screenshares, files, notifications, auth]

for router in routers:
    app.include_router(router.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3001)
