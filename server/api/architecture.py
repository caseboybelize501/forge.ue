"""
Architecture API — Level 7 Server API

Get ProjectSpec for human review (GATE-1).

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- contracts.api.yaml (L0-008)
- ai.architect_agent (L1-001)
"""
from fastapi import APIRouter, HTTPException
from typing import Optional

from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec

router = APIRouter(prefix="/api/projects/{project_id}/architecture", tags=["architecture"])


@router.get("", response_model=ProjectSpec)
async def get_architecture(project_id: str):
    """
    Get architect plan for human review (GATE-1).
    
    Args:
        project_id: Project identifier
        
    Returns:
        ProjectSpec architecture
    """
    pass
