"""
Store API — Level 7 Server API

Get store submission assets.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.store_spec (L0-007)
- engine.store_agent (L6-002)
"""
from fastapi import APIRouter, HTTPException
from typing import Optional, Dict
from datetime import datetime

from contracts.models.game_brief import GameBrief
from contracts.models.store_spec import StoreSubmission, StoreAssets, RatingConfig
from engine.store_agent import StoreAgent

router = APIRouter(prefix="/api/projects/{project_id}/store", tags=["store"])

# In-memory store submission store
_store_submissions: Dict[str, StoreSubmission] = {}


@router.get("", response_model=StoreSubmission)
async def get_store_submission(project_id: str):
    """
    Get store submission assets.

    Args:
        project_id: Project identifier

    Returns:
        Store submission package

    Raises:
        HTTPException: If submission not found
    """
    if project_id not in _store_submissions:
        raise HTTPException(
            status_code=404,
            detail=f"Store submission for project {project_id} not found. Please generate submission first."
        )

    return _store_submissions[project_id]


@router.post("", response_model=StoreSubmission)
async def generate_store_submission(project_id: str, store_platform: str = "steam"):
    """
    Generate store submission assets.

    Args:
        project_id: Project identifier
        store_platform: Store platform (steam, epic, etc.)

    Returns:
        Generated StoreSubmission

    Raises:
        HTTPException: If submission generation fails
    """
    try:
        # Initialize store agent
        store_agent = StoreAgent()

        # Generate store submission
        submission = store_agent.generate_submission(project_id, store_platform)

        # Store submission
        _store_submissions[project_id] = submission

        return submission
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate store submission: {str(e)}"
        )


@router.get("/assets", response_model=StoreAssets)
async def get_store_assets(project_id: str):
    """
    Get store assets (screenshots, icons, etc.).

    Args:
        project_id: Project identifier

    Returns:
        Store assets

    Raises:
        HTTPException: If assets not found
    """
    if project_id not in _store_submissions:
        raise HTTPException(
            status_code=404,
            detail=f"Store assets for project {project_id} not found"
        )

    return _store_submissions[project_id].assets


@router.get("/rating", response_model=RatingConfig)
async def get_rating_config(project_id: str):
    """
    Get rating configuration (ESRB, PEGI, etc.).

    Args:
        project_id: Project identifier

    Returns:
        Rating configuration

    Raises:
        HTTPException: If rating config not found
    """
    if project_id not in _store_submissions:
        raise HTTPException(
            status_code=404,
            detail=f"Rating config for project {project_id} not found"
        )

    return _store_submissions[project_id].rating
