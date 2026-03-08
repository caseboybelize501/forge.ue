"""
Agent Message Schema — Level 0 Foundation

Defines schemas for inter-agent communication.

Dependencies: None (foundation file)
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class AgentTask(BaseModel):
    """
    Task assignment for an agent.
    
    Attributes:
        task_id: Unique task identifier
        agent_type: Type of agent (architect, test, repair, etc.)
        input_data: Task input data dictionary
        priority: Task priority (0 = lowest)
        deadline: Optional task deadline
    """
    task_id: str
    agent_type: str
    input_data: Dict[str, Any]
    priority: int = 0
    deadline: Optional[datetime] = None
    
    @field_validator('task_id')
    @classmethod
    def task_id_not_empty(cls, v: str) -> str:
        """Validate task_id is not empty."""
        if not v or not v.strip():
            raise ValueError('task_id cannot be empty')
        return v.strip()
    
    @field_validator('agent_type')
    @classmethod
    def agent_type_not_empty(cls, v: str) -> str:
        """Validate agent_type is not empty."""
        if not v or not v.strip():
            raise ValueError('agent_type cannot be empty')
        return v.strip()
    
    @field_validator('priority')
    @classmethod
    def priority_non_negative(cls, v: int) -> int:
        """Validate priority is non-negative."""
        if v < 0:
            raise ValueError('priority must be non-negative')
        return v


class AgentResult(BaseModel):
    """
    Result from agent execution.
    
    Attributes:
        task_id: Reference to original task
        success: Whether agent execution succeeded
        output_data: Agent output data dictionary
        errors: List of error messages
        duration_seconds: Execution duration
    """
    task_id: str
    success: bool
    output_data: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    duration_seconds: float = 0.0
    
    @field_validator('task_id')
    @classmethod
    def task_id_not_empty(cls, v: str) -> str:
        """Validate task_id is not empty."""
        if not v or not v.strip():
            raise ValueError('task_id cannot be empty')
        return v.strip()
    
    @field_validator('duration_seconds')
    @classmethod
    def duration_non_negative(cls, v: float) -> float:
        """Validate duration is non-negative."""
        if v < 0:
            raise ValueError('duration_seconds must be non-negative')
        return v


class CriticResult(BaseModel):
    """
    Result from critic gate evaluation.
    
    Attributes:
        phase: Phase number being evaluated
        passed: Whether the phase passed
        pass_results: Results per pass (pass1, pass2, etc.)
        errors: List of error messages
        warnings: List of warning messages
        timestamp: Evaluation timestamp
    """
    phase: int
    passed: bool
    pass_results: Dict[str, bool] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    timestamp: datetime
    
    @field_validator('phase')
    @classmethod
    def phase_non_negative(cls, v: int) -> int:
        """Validate phase is non-negative."""
        if v < 0:
            raise ValueError('phase must be non-negative')
        return v
