from sqlalchemy.orm import Session
from BackEnd.models import Project
from BackEnd.schemas import ProjectCreate, ProjectUpdate

def create_project(db: Session, project: ProjectCreate) -> Project:
    db_project = Project(
        title=project.title,
        start_date=project.start_date,
        end_date=project.end_date,
        description=project.description,
        owner_id=project.owner_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_project(db: Session, project_id: int) -> Project:
    return db.query(Project).filter(Project.id == project_id).first()

def delete_project(db: Session, project: Project):
    db.delete(project)
    db.commit()
