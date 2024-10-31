from pydantic import BaseModel
from typing import List, Optional

class Employee(BaseModel):
    name: str
    position: str
    photo: str
    project_id: Optional[int]

    class Config:
        orm_mode = True

class Project(BaseModel):
    name: str
    description: str
    workers: List[Employee]

    class Config:
        orm_mode = True

class CreateEmployee(Employee):
    pass

class CreateProject(BaseModel):
    name: str
    description: str
    workers: Optional[List[int]] = []
