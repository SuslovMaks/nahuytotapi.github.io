from fastapi import FastAPI, Depends
from typing import List
from sqlalchemy.orm import Session

from models import Base, Employee, Project
from database import engine, session_local
from schemas import Employee as EmpDB, Project as ProDB, CreateProject, CreateEmployee

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.post("/project/", response_model=ProDB)
async def create_project(project: CreateProject, db: Session = Depends(get_db)) -> ProDB:
    db_project = Project(name=project.name, description=project.description)

    if project.workers:
        workers = db.query(Employee).filter(Employee.id.in_(project.workers)).all()
        db_project.workers.extend(workers)

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.post("/employee/", response_model=EmpDB)
async def create_employee(employee: CreateEmployee, db: Session = Depends(get_db)) -> EmpDB:
    db_employee = Employee(name=employee.name, position=employee.position, photo=employee.photo, project_id=employee.project_id)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employee/", response_model=List[EmpDB])
async def read_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return employees

@app.get("/projects/", response_model=List[ProDB])
async def read_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects
