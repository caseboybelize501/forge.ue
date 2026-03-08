"""
Build History Model — Level 7 Server Models

Build history database model.
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from server.models.database import Base


class BuildHistory(Base):
    """
    Build History database model.
    
    Attributes:
        id: Primary key
        project_id: Foreign key to projects
        configuration: Build configuration
        success: Build success status
        errors: Error list JSON
        duration_seconds: Build duration
        created_at: Build timestamp
    """
    __tablename__ = "build_history"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    configuration = Column(String)
    success = Column(Boolean, default=False)
    errors = Column(JSON)
    duration_seconds = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project", back_populates="builds")
