from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

#Database Imports
from .database import engine, get_db
from sqlalchemy.orm import Session

#Model Imports
from .models import vendor

#Router Imports
from .router import user, menu


app = FastAPI()

#Cors Header
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vendor.Base.metadata.create_all(bind=engine)

app.add_middleware(SessionMiddleware ,secret_key='thisismysecret', session_cookie='cookie22')

#Test Routes to check Server is runing
@app.get("/", tags=["test"], description="To check if server is runing")
async def root():
    return {"message": "Server Runing!"}

app.include_router(user.router)
app.include_router(menu.router)