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

def update_user(db: Session, db_user: User, user_update: UserUpdate):

    #اول چک میکنیم که چیا در مدلمون نوشته شده تا اونارو در دیتابیس عوض کنیم
    if user_update.name:
        db_user.name = user_update.name
    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.hashed_password = Hash.bcrypt(user_update.password)
    if user_update.role and db_user.role != UserRole.admin:
        db_user.role = user_update.role


    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
    return {"detail": "کاربر با موفقیت حذف شد."}