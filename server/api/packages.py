"""
Packages API — Level 7 Server API

Platform packaging and download.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.platform_spec (L0-006)
- contracts.api.yaml (L0-008)
- engine.package_agent (L6-001)
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from typing import List

from contracts.models.game_brief import Platform
from contracts.models.platform_spec import PlatformTarget, PackageResult
from contracts.models.build_result import TaskResponse

router = APIRouter(prefix="/api/projects/{project_id}/package", tags=["packages"])


@router.post("", response_model=TaskResponse)
async def trigger_packaging(project_id: str, platforms: List[str], background_tasks: BackgroundTasks):
    """
    Trigger platform packaging.
    
    Args:
        project_id: Project identifier
        platforms: List of platform names
        background_tasks: FastAPI background tasks
        
    Returns:
        Task response
    """
    pass


@router.get("/{platform}")
async def download_package(project_id: str, platform: str):
    """
    Download packaged binary.
    
    Args:
        project_id: Project identifier
        platform: Platform name
        
    Returns:
        Package file download
    """
    pass
