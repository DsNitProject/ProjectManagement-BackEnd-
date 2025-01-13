import uvicorn
from fastapi import FastAPI
from pip._internal.network import auth

from BackEnd import models
from BackEnd.routers import authuser, users
from database.database import engine, Base

models.Base.metadata.create_all(bind=engine)



app = FastAPI()

app.include_router(authuser.router)
app.include_router(users.router)
@app.get("/")
async def root():
    return {"Hello": "World"}
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7000)
