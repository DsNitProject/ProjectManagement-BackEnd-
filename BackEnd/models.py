from sqlalchemy import Column, Integer, String,Enum as sqlEnum
from BackEnd.database.database import Base
from enum import Enum



class UserRole(Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(sqlEnum(UserRole), default=UserRole.user, nullable=False)

