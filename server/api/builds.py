"""
Builds API — Level 7 Server API

Get compilation status and error logs.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.build_result (L0-004)
- contracts.api.yaml (L0-008)
- engine.build_runner (L5-001)
"""
from fastapi import APIRouter, HTTPException

from contracts.models.game_brief import GameBrief
from contracts.models.build_result import CompileResult, TestResult, BuildStatusResponse

router = APIRouter(prefix="/api/projects/{project_id}/build", tags=["builds"])


@router.get("", response_model=BuildStatusResponse)
async def get_build_status(project_id: str):
    """
    Get compilation status.
    
    Args:
        project_id: Project identifier
        
    Returns:
        Build status response
    """
    pass
