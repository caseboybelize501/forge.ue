"""
FORGE Contracts Package

Pydantic schemas for pipeline data models.

Dependencies: All contracts.models.* modules
"""
from contracts.models.game_brief import (
    GameBrief, Genre, Platform, MechanicSpec, GameBriefRequest
)
from contracts.models.project_spec import (
    ProjectSpec, ModuleSpec, SubsystemRef, ModuleType, Pattern
)
from contracts.models.code_artifact import (
    CppFile, HeaderFile, BlueprintGraph, BlueprintNode
)
from contracts.models.build_result import (
    CompileResult, TestResult, PackageResult,
    ErrorReport, RepairContext, TestSpec,
    ProjectResponse, TaskResponse, ProgressResponse,
    FileTreeResponse, BuildStatusResponse, CriticLogResponse
)
from contracts.models.agent_message import (
    AgentTask, AgentResult, CriticResult
)
from contracts.models.platform_spec import (
    PlatformTarget, SDKStatus, PackageConfig, PlatformSpec
)
from contracts.models.store_spec import (
    StoreSubmission, StoreAssets, RatingConfig, StorePlatform, RatingBoard
)

__all__ = [
    # Game Brief
    'GameBrief', 'Genre', 'Platform', 'MechanicSpec', 'GameBriefRequest',
    # Project Spec
    'ProjectSpec', 'ModuleSpec', 'SubsystemRef', 'ModuleType', 'Pattern',
    # Code Artifact
    'CppFile', 'HeaderFile', 'BlueprintGraph', 'BlueprintNode',
    # Build Result
    'CompileResult', 'TestResult', 'PackageResult',
    'ErrorReport', 'RepairContext', 'TestSpec',
    'ProjectResponse', 'TaskResponse', 'ProgressResponse',
    'FileTreeResponse', 'BuildStatusResponse', 'CriticLogResponse',
    # Agent Message
    'AgentTask', 'AgentResult', 'CriticResult',
    # Platform Spec
    'PlatformTarget', 'SDKStatus', 'PackageConfig', 'PlatformSpec',
    # Store Spec
    'StoreSubmission', 'StoreAssets', 'RatingConfig', 'StorePlatform', 'RatingBoard',
]
