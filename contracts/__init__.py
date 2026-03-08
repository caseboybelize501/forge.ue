"""
FORGE Contracts Package

Pydantic schemas for pipeline data models.

Dependencies: contracts.models
"""
from contracts.models import (
    GameBrief, Genre, Platform, MechanicSpec, GameBriefRequest,
    ProjectSpec, ModuleSpec, SubsystemRef, ModuleType, Pattern,
    CppFile, HeaderFile, BlueprintGraph, BlueprintNode,
    CompileResult, TestResult, PackageResult,
    ErrorReport, RepairContext, TestSpec,
    ProjectResponse, TaskResponse, ProgressResponse,
    FileTreeResponse, BuildStatusResponse, CriticLogResponse,
    AgentTask, AgentResult, CriticResult,
    PlatformTarget, SDKStatus, PackageConfig, PlatformSpec,
    StoreSubmission, StoreAssets, RatingConfig, StorePlatform, RatingBoard,
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
