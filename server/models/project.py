"""
Project Model — Level 7 Server Models

Project database model.
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from server.models.database import Base


class ProjectStatus(str, enum.Enum):
    """Project status enumeration."""
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Project(Base):
    """
    Project database model.
    
    Attributes:
        id: Primary key
        name: Project name
        brief: Game brief JSON
        spec: ProjectSpec JSON
        status: Current status
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brief = Column(JSON)
    spec = Column(JSON)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.CREATED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    builds = relationship("BuildHistory", back_populates="project")
