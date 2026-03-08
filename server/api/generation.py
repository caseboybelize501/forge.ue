"""
Generation API — Level 7 Server API

Trigger generation and get progress.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- contracts.api.yaml (L0-008)
- engine.cpp_generator (L4-001)
- engine.blueprint_generator (L4-002)
- engine.build_runner (L5-001)
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional

from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec
from contracts.models.build_result import TaskResponse, ProgressResponse, FileTreeResponse

router = APIRouter(prefix="/api/projects/{project_id}/generate", tags=["generation"])


@router.post("", response_model=TaskResponse)
async def trigger_generation(project_id: str, background_tasks: BackgroundTasks):
    """
    Trigger full generation pipeline.
    
    Args:
        project_id: Project identifier
        background_tasks: FastAPI background tasks
        
    Returns:
        Task response
    """
    pass


@router.get("/progress", response_model=ProgressResponse)
async def get_progress(project_id: str):
    """
    Get topo level + critic status.
    
    Args:
        project_id: Project identifier
        
    Returns:
        Progress response
    """
    pass


@router.get("/files", response_model=FileTreeResponse)
async def get_file_tree(project_id: str):
    """
    Get generated file tree.
    
    Args:
        project_id: Project identifier
        
    Returns:
        File tree response
    """
    pass
