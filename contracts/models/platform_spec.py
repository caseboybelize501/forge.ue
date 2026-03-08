"""
Platform Specification Schema — Level 0 Foundation

Defines schemas for platform targets and SDK status.

Dependencies: None (foundation file)
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class PlatformTarget(str, Enum):
    """
    Platform target enumeration per forgeue.md.
    
    Values match UE5 platform naming conventions.
    """
    WIN64 = "Win64"
    MAC = "Mac"
    ANDROID = "Android"
    IOS = "iOS"
    PS5 = "PS5"
    XBOX = "Xbox"
    SWITCH = "Switch"


class SDKStatus(str, Enum):
    """
    SDK availability status.
    
    Used for platform SDK detection and gating.
    """
    AVAILABLE = "available"
    MISSING = "missing"
    PARTIAL = "partial"


class PackageConfig(BaseModel):
    """
    Configuration for platform packaging.
    
    Attributes:
        platform: Target platform
        sdk_path: Path to platform SDK (optional)
        cook_flags: UE5 cook command flags
        pak_flags: UE5 pak command flags
        compression: Compression method (default: Oodle)
    """
    platform: PlatformTarget
    sdk_path: Optional[str] = None
    cook_flags: List[str] = Field(default_factory=list)
    pak_flags: List[str] = Field(default_factory=list)
    compression: str = "Oodle"
    
    @field_validator('platform')
    @classmethod
    def platform_valid(cls, v: PlatformTarget) -> PlatformTarget:
        """Validate platform is supported."""
        supported = [e.value for e in PlatformTarget]
        if v.value not in supported:
            raise ValueError(f'platform must be one of: {supported}')
        return v
    
    @field_validator('compression')
    @classmethod
    def compression_valid(cls, v: str) -> str:
        """Validate compression method."""
        valid_methods = ['Oodle', 'Zlib', 'None']
        if v not in valid_methods:
            raise ValueError(f'compression must be one of: {valid_methods}')
        return v


class PlatformSpec(BaseModel):
    """
    Complete platform specification.
    
    Attributes:
        targets: List of target platforms
        sdk_status: SDK availability per platform
        configs: Packaging configuration per platform
    """
    targets: List[PlatformTarget]
    sdk_status: Dict[PlatformTarget, SDKStatus]
    configs: Dict[PlatformTarget, PackageConfig]
    
    @field_validator('targets')
    @classmethod
    def at_least_one_target(cls, v: List[PlatformTarget]) -> List[PlatformTarget]:
        """Validate at least one target platform."""
        if not v or len(v) == 0:
            raise ValueError('at least one target platform must be specified')
        return v
    
    @field_validator('sdk_status')
    @classmethod
    def sdk_status_complete(cls, v: Dict[PlatformTarget, SDKStatus], info) -> Dict[PlatformTarget, SDKStatus]:
        """Validate SDK status covers all targets."""
        if 'targets' in info.data:
            for target in info.data['targets']:
                if target not in v:
                    raise ValueError(f'sdk_status missing for platform: {target.value}')
        return v
    
    @field_validator('configs')
    @classmethod
    def configs_complete(cls, v: Dict[PlatformTarget, PackageConfig], info) -> Dict[PlatformTarget, PackageConfig]:
        """Validate configs cover all targets."""
        if 'targets' in info.data:
            for target in info.data['targets']:
                if target not in v:
                    raise ValueError(f'config missing for platform: {target.value}')
        return v
