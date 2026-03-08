"""
Build Worker — Level 7 Server Worker

Celery worker for UBT compile and test run.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.build_result (L0-004)
- engine.build_runner (L5-001)
"""
from celery import Celery
from pathlib import Path

from contracts.models.game_brief import GameBrief
from contracts.models.build_result import CompileResult, TestResult

app = Celery("forge", broker="redis://localhost:6379/0")


@app.task
def run_ubt_compile(project_id: str, configuration: str = "Development"):
    """
    Run UBT compile via Celery.
    
    Args:
        project_id: Project identifier
        configuration: Build configuration
    """
    pass


@app.task
def run_tests(project_id: str):
    """
    Run UE5 Automation Tests.
    
    Args:
        project_id: Project identifier
    """
    pass
