"""
Projects API — Level 7 Server API

CRUD operations for projects.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- contracts.models.build_result (L0-004)
- engine.brief_parser (L2-004)
- engine.project_scaffolder (L3-001)
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict
from datetime import datetime
from pathlib import Path

from contracts.models.game_brief import GameBrief, GameBriefRequest
from contracts.models.project_spec import ProjectSpec
from contracts.models.build_result import ProjectResponse
from engine.brief_parser import BriefParser
from engine.project_scaffolder import ProjectScaffolder

router = APIRouter(prefix="/api/projects", tags=["projects"])

# In-memory project store (replace with database in production)
_projects_db: Dict[str, Dict] = {}


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(brief: GameBriefRequest):
    """
    Create project from GameBrief.

    Args:
        brief: Game brief request

    Returns:
        Project response with ID

    Raises:
        HTTPException: If project creation fails
    """
    try:
        # Parse brief
        parser = BriefParser()
        game_brief = parser.parse_brief(brief.brief)

        # Generate project ID
        project_id = f"PROJ_{game_brief.title.upper().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Store project
        _projects_db[project_id] = {
            "project_id": project_id,
            "project_name": game_brief.title,
            "brief": game_brief,
            "status": "created",
            "created_at": datetime.now()
        }

        return ProjectResponse(
            project_id=project_id,
            project_name=game_brief.title,
            status="created",
            created_at=datetime.now()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """
    Get project details.

    Args:
        project_id: Project identifier

    Returns:
        Project details

    Raises:
        HTTPException: If project not found
    """
    if project_id not in _projects_db:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

    project = _projects_db[project_id]
    return ProjectResponse(
        project_id=project["project_id"],
        project_name=project["project_name"],
        status=project["status"],
        created_at=project["created_at"]
    )


@router.get("", response_model=List[ProjectResponse])
async def list_projects():
    """
    List all projects.

    Returns:
        List of project responses
    """
    return [
        ProjectResponse(
            project_id=p["project_id"],
            project_name=p["project_name"],
            status=p["status"],
            created_at=p["created_at"]
        )
        for p in _projects_db.values()
    ]


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: str):
    """
    Delete project.

    Args:
        project_id: Project identifier

    Raises:
        HTTPException: If project not found
    """
    if project_id not in _projects_db:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

    del _projects_db[project_id]
