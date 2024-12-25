from BackEnd.CRUD.user_crud import get_user_by_email, create_user
from BackEnd.schemas import Token, Login, UserCreate, UserRole, UserResponse

from fastapi import APIRouter, Depends, HTTPException, status

from BackEnd.database.database import Session, get_db
from BackEnd.utils.hash import Hash
from BackEnd.utils.jwt_handler import create_access_token

router = APIRouter(prefix="/authuser", tags=["authuser"])

@router.post("/login",response_model=Token)
def login(request:Login,db:Session = Depends(get_db)):
    user=get_user_by_email(db,request.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email")
    if not Hash.verify(request.password,user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect password")
    access_token=create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}




@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user, role=UserRole.user)
