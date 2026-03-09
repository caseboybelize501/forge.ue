"""
Builds API — Level 7 Server API

Get compilation status and error logs.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.build_result (L0-004)
- engine.build_runner (L5-001)
"""
from fastapi import APIRouter, HTTPException
from typing import Optional, Dict
from datetime import datetime
from pathlib import Path

from contracts.models.game_brief import GameBrief
from contracts.models.build_result import CompileResult, TestResult, BuildStatusResponse, ErrorReport
from engine.build_runner import BuildRunner

router = APIRouter(prefix="/api/projects/{project_id}/build", tags=["builds"])

# In-memory build state store
_build_state: Dict[str, Dict] = {}


@router.get("", response_model=BuildStatusResponse)
async def get_build_status(project_id: str):
    """
    Get compilation status.

    Args:
        project_id: Project identifier

    Returns:
        Build status response

    Raises:
        HTTPException: If build state not found
    """
    if project_id not in _build_state:
        # Return empty build status
        return BuildStatusResponse(
            success=False,
            errors=[],
            warnings=[],
            duration_seconds=0.0
        )

    state = _build_state[project_id]
    return BuildStatusResponse(
        success=state.get("success", False),
        errors=state.get("errors", []),
        warnings=state.get("warnings", []),
        duration_seconds=state.get("duration_seconds", 0.0)
    )


@router.post("/compile", response_model=BuildStatusResponse)
async def compile_project(project_id: str, configuration: str = "Development"):
    """
    Trigger project compilation.

    Args:
        project_id: Project identifier
        configuration: Build configuration (Development, Shipping, etc.)

    Returns:
        Build status response

    Raises:
        HTTPException: If compilation fails
    """
    try:
        # Get project path (from project store)
        project_path = Path("output") / project_id
        if not project_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Project {project_id} not found"
            )

        # Initialize build runner
        ue_root = Path("C:/UnrealEngine")  # Configurable
        runner = BuildRunner(ue_root=ue_root)

        # Run UHT
        uht_result = runner.run_uht(project_path)
        if not uht_result.success:
            _build_state[project_id] = {
                "success": False,
                "errors": uht_result.errors,
                "warnings": uht_result.warnings,
                "duration_seconds": uht_result.duration_seconds
            }
            return BuildStatusResponse(
                success=False,
                errors=uht_result.errors,
                warnings=uht_result.warnings,
                duration_seconds=uht_result.duration_seconds
            )

        # Run UBT
        ubt_result = runner.run_ubt(project_path, configuration)
        _build_state[project_id] = {
            "success": ubt_result.success,
            "errors": ubt_result.errors,
            "warnings": ubt_result.warnings,
            "duration_seconds": ubt_result.duration_seconds
        }

        return BuildStatusResponse(
            success=ubt_result.success,
            errors=ubt_result.errors,
            warnings=ubt_result.warnings,
            duration_seconds=ubt_result.duration_seconds
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Compilation failed: {str(e)}"
        )
