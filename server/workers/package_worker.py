"""
Package Worker — Level 7 Server Worker

Celery worker for cook + pak per platform.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.platform_spec (L0-006)
- engine.package_agent (L6-001)
"""
from celery import Celery
from pathlib import Path

from contracts.models.game_brief import Platform
from contracts.models.platform_spec import PlatformTarget
from contracts.models.build_result import PackageResult

app = Celery("forge", broker="redis://localhost:6379/0")


@app.task
def package_platform(project_id: str, platform: str):
    """
    Package project for single platform.
    
    Args:
        project_id: Project identifier
        platform: Platform name
    """
    pass
