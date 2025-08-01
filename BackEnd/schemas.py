from datetime import date
from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.user

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    role: Optional[UserRole]

class UserResponse(UserBase):
    id: int
    role: UserRole

class Login(BaseModel):
    email: EmailStr
    password: str
class ProjectBase(BaseModel):
    title: str
    start_date: date
    end_date: date
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    owner_id: int

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    owner: UserResponse
    tasks: List['TaskResponse'] = []

    class Config:
        orm_mode = True



class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class TaskPriority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.normal
    deadline: Optional[datetime] = None
    project_id: int
    assignee_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus]
    priority: Optional[TaskPriority]
    deadline: Optional[datetime]
    project_id: Optional[int]
    assignee_id: Optional[int]

class TaskResponse(TaskBase):
    id: int

    class Config:
        orm_mode = True
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    user_id: Optional[int] = None


ProjectResponse.update_forward_refs()
TaskResponse.update_forward_refs()