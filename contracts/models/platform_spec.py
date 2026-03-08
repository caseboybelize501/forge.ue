"""
Platform Specification Schema — Level 0 Foundation

Defines schemas for platform targets and SDK status.
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class PlatformTarget(str, Enum):
    """Platform target enumeration."""
    WIN64 = "Win64"
    MAC = "Mac"
    ANDROID = "Android"
    IOS = "iOS"
    PS5 = "PS5"
    XBOX = "Xbox"
    SWITCH = "Switch"


class SDKStatus(str, Enum):
    """SDK availability status."""
    AVAILABLE = "available"
    MISSING = "missing"
    PARTIAL = "partial"


class PackageConfig(BaseModel):
    """Configuration for platform packaging."""
    platform: PlatformTarget
    sdk_path: Optional[str]
    cook_flags: List[str] = []
    pak_flags: List[str] = []
    compression: str = "Oodle"


class PlatformSpec(BaseModel):
    """Complete platform specification."""
    targets: List[PlatformTarget]
    sdk_status: Dict[PlatformTarget, SDKStatus]
    configs: Dict[PlatformTarget, PackageConfig]
