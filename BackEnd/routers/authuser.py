from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from BackEnd.database.database import Session, get_db
from BackEnd.routers.oauth2 import oauth2_scheme
from BackEnd.schemas.user import UserRegister

router = APIRouter(prefix="/authuser", tags=["authuser"])

@router.post("/token")
def get_token(request: OAuth2PasswordRequestForm = Depends()):
    access_token=oauth2_scheme.create_access_token()
    return {"access_token": access_token, "token_type": "bearer"}
