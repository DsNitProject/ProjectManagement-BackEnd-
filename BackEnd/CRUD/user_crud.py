from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from BackEnd.models import User, UserRole
from BackEnd.schemas import UserCreate, UserUpdate
from BackEnd.utils.hash import Hash


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate, role: UserRole = UserRole.user):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=404, detail="ایمیل قبلا ثبت ‌نام شده است.")

    hashed_password = Hash.bcrypt(user.password) #هش کردن پسورد برای سیو کرد در دیتابیس
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #این برای برگرداندن ایدی ای که دیتابیس ساخته هستش
    return new_user