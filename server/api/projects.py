"""
Projects API — Level 7 Server API

CRUD operations for projects.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- contracts.api.yaml (L0-008)
- engine.brief_parser (L2-004)
- engine.project_scaffolder (L3-001)
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pathlib import Path
from datetime import datetime

from contracts.models.game_brief import GameBrief, GameBriefRequest
from contracts.models.project_spec import ProjectSpec
from contracts.models.build_result import ProjectResponse

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(brief: GameBriefRequest):
    """
    Create project from GameBrief.
    
    Args:
        brief: Game brief request
        
    Returns:
        Project response with ID
    """
    pass


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """
    Get project details.
    
    Args:
        project_id: Project identifier
        
    Returns:
        Project details
    """
    pass
