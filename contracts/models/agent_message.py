"""
Agent Message Schema — Level 0 Foundation

Defines schemas for inter-agent communication.
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class AgentTask(BaseModel):
    """Task assignment for an agent."""
    task_id: str
    agent_type: str
    input_data: Dict[str, Any]
    priority: int = 0
    deadline: Optional[datetime] = None


class AgentResult(BaseModel):
    """Result from agent execution."""
    task_id: str
    success: bool
    output_data: Dict[str, Any]
    errors: List[str] = []
    duration_seconds: float = 0.0


class CriticResult(BaseModel):
    """Result from critic gate evaluation."""
    phase: int
    passed: bool
    pass_results: Dict[str, bool]
    errors: List[str] = []
    warnings: List[str] = []
    timestamp: datetime
