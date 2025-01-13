from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from BackEnd.CRUD.project_crud import *
from BackEnd.routers.users import get_current_user
from BackEnd.schemas import ProjectCreate, ProjectResponse, UserRole
from BackEnd.database.database import get_db
from BackEnd.models import Project, User
from BackEnd.DataStructures.HashMap import HashMap
from BackEnd.utils.jwt_bearer import JWTBearer

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    dependencies=[Depends(JWTBearer())]
)

project_map = HashMap()


@router.post("/", response_model=ProjectResponse)
def create_new_project(project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin.value:
        raise HTTPException(status_code=403, detail="دسترسی غیرمجاز")
    new_project = create_project(db, project)
    project_map.set(new_project.id, new_project)
    return new_project

@router.get("/", response_model=List[ProjectResponse])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = get_projects(db, skip=skip, limit=limit)
    for project in projects:
        project_map.set(project.id, project)
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = project_map.get(project_id)
    if not project:
        project = get_project(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="پروژه یافت نشد")
        project_map.set(project_id, project)
    return project
