"""
FORGE Contracts Package

Pydantic schemas for pipeline data models.
"""
from contracts.models.game_brief import GameBrief, Genre, Platform, MechanicSpec
from contracts.models.project_spec import ProjectSpec, ModuleSpec, SubsystemRef, ModuleType, Pattern
from contracts.models.code_artifact import CppFile, HeaderFile, BlueprintGraph, BlueprintNode
from contracts.models.build_result import (
    CompileResult, TestResult, PackageResult,
    ErrorReport, RepairContext, TestSpec
)
from contracts.models.agent_message import AgentTask, AgentResult, CriticResult
from contracts.models.platform_spec import PlatformTarget, SDKStatus, PackageConfig, PlatformSpec
from contracts.models.store_spec import StoreSubmission, StoreAssets, RatingConfig

__all__ = [
    # Game Brief
    'GameBrief', 'Genre', 'Platform', 'MechanicSpec',
    # Project Spec
    'ProjectSpec', 'ModuleSpec', 'SubsystemRef', 'ModuleType', 'Pattern',
    # Code Artifact
    'CppFile', 'HeaderFile', 'BlueprintGraph', 'BlueprintNode',
    # Build Result
    'CompileResult', 'TestResult', 'PackageResult', 'ErrorReport', 'RepairContext', 'TestSpec',
    # Agent Message
    'AgentTask', 'AgentResult', 'CriticResult',
    # Platform Spec
    'PlatformTarget', 'SDKStatus', 'PackageConfig', 'PlatformSpec',
    # Store Spec
    'StoreSubmission', 'StoreAssets', 'RatingConfig',
]
