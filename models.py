from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    position = Column(String, index=True)
    photo = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="workers")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    workers = relationship("Employee", back_populates="project")
