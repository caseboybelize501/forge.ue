"""
Packages API — Level 7 Server API

Platform packaging and download.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.platform_spec (L0-006)
- contracts.models.build_result (L0-004)
- engine.package_agent (L6-001)
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from contracts.models.game_brief import Platform
from contracts.models.platform_spec import PlatformTarget
from contracts.models.build_result import TaskResponse, PackageResult

router = APIRouter(prefix="/api/projects/{project_id}/package", tags=["packages"])

# In-memory packaging state store
_package_state: Dict[str, Dict] = {}


async def _run_packaging(project_id: str, platforms: List[str]):
    """
    Run packaging pipeline in background.

    Args:
        project_id: Project identifier
        platforms: List of platform names
    """
    state = _package_state[project_id]
    state["status"] = "running"
    state["platforms"] = platforms

    try:
        # Package each platform
        for platform in platforms:
            state["current_platform"] = platform
            state["status"] = f"packaging_{platform.lower()}"

            # Simulate packaging (replace with actual package_agent call)
            # package_agent = PackageAgent()
            # result = package_agent.cook_and_pak(platform)

        state["status"] = "complete"
        state["completed_at"] = datetime.now()
    except Exception as e:
        state["status"] = "failed"
        state["error"] = str(e)


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

    Raises:
        HTTPException: If project not found or packaging already running
    """
    if project_id in _package_state and _package_state[project_id]["status"] == "running":
        raise HTTPException(
            status_code=400,
            detail="Packaging already in progress for this project"
        )

    # Validate platforms
    valid_platforms = ["Win64", "Mac", "Android", "iOS", "PS5", "Xbox", "Switch"]
    for platform in platforms:
        if platform not in valid_platforms:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid platform: {platform}. Valid platforms: {valid_platforms}"
            )

    # Initialize packaging state
    _package_state[project_id] = {
        "project_id": project_id,
        "status": "queued",
        "platforms": [],
        "current_platform": None,
        "started_at": datetime.now()
    }

    # Queue background task
    background_tasks.add_task(_run_packaging, project_id, platforms)

    return TaskResponse(
        task_id=f"PKG_{project_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        status="queued",
        message=f"Packaging queued for platforms: {', '.join(platforms)}"
    )


@router.get("/{platform}", response_class=FileResponse)
async def download_package(project_id: str, platform: str):
    """
    Download packaged binary.

    Args:
        project_id: Project identifier
        platform: Platform name

    Returns:
        Package file download

    Raises:
        HTTPException: If package not found or not ready
    """
    if project_id not in _package_state:
        raise HTTPException(
            status_code=404,
            detail=f"No packaging state found for project {project_id}"
        )

    state = _package_state[project_id]
    if state["status"] != "complete":
        raise HTTPException(
            status_code=400,
            detail="Packaging not yet complete"
        )

    if platform not in state["platforms"]:
        raise HTTPException(
            status_code=404,
            detail=f"Package for platform {platform} not found"
        )

    # Return package file (replace with actual file path)
    package_path = Path("output") / project_id / "Binaries" / platform / f"{project_id}.zip"
    if not package_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Package file not found"
        )

    return FileResponse(
        path=str(package_path),
        media_type="application/zip",
        filename=f"{project_id}_{platform}.zip"
    )


@router.get("/status", response_model=Dict)
async def get_packaging_status(project_id: str):
    """
    Get packaging status.

    Args:
        project_id: Project identifier

    Returns:
        Packaging status

    Raises:
        HTTPException: If packaging state not found
    """
    if project_id not in _package_state:
        raise HTTPException(
            status_code=404,
            detail=f"No packaging state found for project {project_id}"
        )

    return _package_state[project_id]
