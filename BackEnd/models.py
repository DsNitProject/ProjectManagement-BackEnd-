from sqlalchemy import Column, Integer, String, Enum as sqlEnum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from BackEnd.database.database import Base
from enum import Enum



class UserRole(Enum):
    admin = "admin"
    user = "user"

class TaskStatus(Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class TaskPriority(Enum):
    low = "low"
    normal = "normal"
    high = "high"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(sqlEnum(UserRole), default=UserRole.user, nullable=False)
    tasks = relationship("Task", back_populates="assignee")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    tasks = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(sqlEnum(TaskStatus), default=TaskStatus.pending, nullable=False)
    priority = Column(sqlEnum(TaskPriority), default=TaskPriority.normal, nullable=False)
    deadline = Column(DateTime, nullable=True)

    project_id = Column(Integer, ForeignKey("projects.id"))
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")
