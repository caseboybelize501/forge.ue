"""
Architecture API — Level 7 Server API

Get ProjectSpec for human review (GATE-1).

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- ai.architect_agent (L1-001)
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from pathlib import Path

from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec
from ai.architect_agent import ArchitectAgent

router = APIRouter(
    prefix="/api/projects/{project_id}/architecture",
    tags=["architecture"]
)

# In-memory architecture store (replace with database in production)
_architecture_db = {}


@router.get("", response_model=ProjectSpec)
async def get_architecture(project_id: str):
    """
    Get architect plan for human review (GATE-1).

    Args:
        project_id: Project identifier

    Returns:
        ProjectSpec architecture

    Raises:
        HTTPException: If architecture not found
    """
    if project_id not in _architecture_db:
        raise HTTPException(
            status_code=404,
            detail=f"Architecture for project {project_id} not found. Please create project first."
        )

    return _architecture_db[project_id]


@router.post("", response_model=ProjectSpec)
async def generate_architecture(project_id: str, brief: GameBrief):
    """
    Generate architecture from GameBrief.

    Args:
        project_id: Project identifier
        brief: Game brief

    Returns:
        Generated ProjectSpec

    Raises:
        HTTPException: If architecture generation fails
    """
    try:
        # Initialize architect agent
        templates_dir = Path("templates")
        architect = ArchitectAgent(templates_dir=templates_dir)

        # Generate architecture
        project_spec = architect.design_architecture(brief)

        # Store architecture
        _architecture_db[project_id] = project_spec

        return project_spec
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate architecture: {str(e)}"
        )
