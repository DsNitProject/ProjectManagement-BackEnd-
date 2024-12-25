from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from BackEnd.CRUD.user_crud import get_user, update_user, delete_user
from BackEnd.database.database import get_db
from BackEnd.schemas import UserCreate, UserResponse, UserUpdate
from BackEnd.models import User, UserRole
from BackEnd.utils.jwt_bearer import JWTBearer
from BackEnd.utils.jwt_handler import decode_jwt_token

router = APIRouter(
    prefix="/users",
    dependencies=[Depends(JWTBearer())]
)

def admin_required(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)): #برای گت هایی است که به دسترسی ادمین نیاز دارن
    payload = decode_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user or user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user

@router.get("/{user_id}", response_model=UserResponse)
def get_specefic_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    payload = decode_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid token")
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid user")
    target_user = get_user(db, user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role != UserRole.admin and user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this user")
    return target_user
