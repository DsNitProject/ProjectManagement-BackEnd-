from sqlalchemy import Column, Integer, String, Enum as sqlEnum, DateTime, ForeignKey, Date, Text
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
    projects = relationship("Project", back_populates="owner")
    tasks = relationship("Task", back_populates="assignee")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False, default=TaskStatus.pending.value)  # "pending"، "in_progress"، "done"
    priority = Column(String, nullable=False, default=TaskPriority.normal.value)  # "low"، "normal"، "high"
    deadline = Column(Date, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    assignee_id = Column(Integer, ForeignKey("users.id"))

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")
