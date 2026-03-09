"""
Generation API — Level 7 Server API

Trigger generation and get progress.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- contracts.models.build_result (L0-004)
- engine.cpp_generator (L4-001)
- engine.blueprint_generator (L4-002)
- engine.build_runner (L5-001)
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional, Dict, List
from datetime import datetime
from pathlib import Path

from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec
from contracts.models.build_result import TaskResponse, ProgressResponse, FileTreeResponse
from engine.cpp_generator import CppGenerator
from engine.blueprint_generator import BlueprintGenerator

router = APIRouter(prefix="/api/projects/{project_id}/generate", tags=["generation"])

# In-memory generation state store
_generation_state: Dict[str, Dict] = {}


async def _run_generation_pipeline(project_id: str, project_spec: ProjectSpec):
    """
    Run full generation pipeline in background.

    Args:
        project_id: Project identifier
        project_spec: Project specification
    """
    state = _generation_state[project_id]
    state["status"] = "running"
    state["current_level"] = 0
    state["total_levels"] = 9

    try:
        # Initialize generators
        cpp_gen = CppGenerator()
        bp_gen = BlueprintGenerator()

        # Generate C++ files
        state["current_level"] = 4
        state["status"] = "generating_cpp"
        cpp_files = cpp_gen.generate_from_spec(project_spec)

        # Generate Blueprint files
        state["current_level"] = 5
        state["status"] = "generating_blueprint"
        for module in project_spec.modules:
            bp_graphs = bp_gen.generate_from_module(module)

        # Generation complete
        state["status"] = "complete"
        state["current_level"] = 9
        state["files_generated"] = len(cpp_files)
    except Exception as e:
        state["status"] = "failed"
        state["error"] = str(e)


@router.post("", response_model=TaskResponse)
async def trigger_generation(project_id: str, background_tasks: BackgroundTasks):
    """
    Trigger full generation pipeline.

    Args:
        project_id: Project identifier
        background_tasks: FastAPI background tasks

    Returns:
        Task response

    Raises:
        HTTPException: If project not found or generation already running
    """
    if project_id in _generation_state and _generation_state[project_id]["status"] == "running":
        raise HTTPException(
            status_code=400,
            detail="Generation already in progress for this project"
        )

    # Initialize generation state
    _generation_state[project_id] = {
        "project_id": project_id,
        "status": "queued",
        "current_level": 0,
        "total_levels": 9,
        "files_generated": 0,
        "started_at": datetime.now()
    }

    # Get project spec (from architecture store)
    from server.api.architecture import _architecture_db
    if project_id not in _architecture_db:
        raise HTTPException(
            status_code=404,
            detail=f"Project spec not found for {project_id}"
        )

    project_spec = _architecture_db[project_id]

    # Queue background task
    background_tasks.add_task(_run_generation_pipeline, project_id, project_spec)

    return TaskResponse(
        task_id=f"GEN_{project_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        status="queued",
        message="Generation pipeline queued"
    )


@router.get("/progress", response_model=ProgressResponse)
async def get_progress(project_id: str):
    """
    Get topo level + critic status.

    Args:
        project_id: Project identifier

    Returns:
        Progress response

    Raises:
        HTTPException: If generation state not found
    """
    if project_id not in _generation_state:
        raise HTTPException(
            status_code=404,
            detail=f"No generation state found for project {project_id}"
        )

    state = _generation_state[project_id]
    return ProgressResponse(
        current_level=state["current_level"],
        total_levels=state["total_levels"],
        critic_status=state["status"],
        files_generated=state.get("files_generated", 0)
    )


@router.get("/files", response_model=FileTreeResponse)
async def get_file_tree(project_id: str):
    """
    Get generated file tree.

    Args:
        project_id: Project identifier

    Returns:
        File tree response

    Raises:
        HTTPException: If generation not complete
    """
    if project_id not in _generation_state:
        raise HTTPException(
            status_code=404,
            detail=f"No generation state found for project {project_id}"
        )

    state = _generation_state[project_id]
    if state["status"] != "complete":
        raise HTTPException(
            status_code=400,
            detail="Generation not yet complete"
        )

    # Return mock file tree (replace with actual file system scan)
    return FileTreeResponse(
        files=[
            {"path": f"Source/{project_id}Core/{project_id}Core.h", "type": "header"},
            {"path": f"Source/{project_id}Core/{project_id}Core.cpp", "type": "cpp"},
            {"path": f"Content/Blueprints/{project_id}_BP.json", "type": "blueprint"},
        ]
    )
