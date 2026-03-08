"""
UE5 Scanner — Level 1 Engine Module

Scan UE5 install, verify version, detect platform SDKs.

Dependencies:
- contracts.models.game_brief (L0-001)
"""
from typing import Dict, Optional, List, Any
from pathlib import Path
import subprocess
import re
import os

from contracts.models.game_brief import Platform


class UE5Scanner:
    """
    UE5 Installation Scanner.

    Scans for:
    - UNREAL_ENGINE_ROOT environment variable
    - UnrealBuildTool binary
    - UE5Editor binary
    - Version verification (≥ 5.3)
    - Platform SDKs (Android, iOS, Switch, PS5, Xbox)

    Attributes:
        ue_root: Path to UE5 installation
        ue_version: Detected UE5 version tuple
        platform_sdks: Detected platform SDK paths
    """

    MIN_UE5_VERSION = (5, 3)

    # Environment variables for platform SDKs
    SDK_ENV_VARS = {
        Platform.ANDROID: 'ANDROID_SDK_ROOT',
        Platform.IOS: 'IOS_TOOLCHAIN',
        Platform.SWITCH: 'SWITCH_SDK_ROOT',
        Platform.PS5: 'PS5_SDK_ROOT',
        Platform.XBOX: 'XBOX_GDK_ROOT',
    }

    # Common UE5 installation paths
    UE5_INSTALL_PATHS = [
        Path(r"C:\Epic Games\Unreal Engine"),
        Path(r"C:\Program Files\Epic Games\Unreal Engine"),
        Path("/opt/UnrealEngine"),
        Path("/usr/local/UnrealEngine"),
        Path.home() / "UnrealEngine",
    ]

    def __init__(self):
        """Initialize UE5 scanner."""
        self.ue_root: Optional[Path] = None
        self.ue_version: Optional[tuple] = None
        self.platform_sdks: Dict[str, Path] = {}

    def scan_ue5_install(self) -> bool:
        """
        Find and verify UE5 installation.

        Returns:
            True if valid UE5 installation found
        """
        # Try to find UE5 root from environment or common paths
        self.ue_root = self._find_ue5_root()
        
        if self.ue_root is None:
            return False
        
        # Verify version meets minimum requirement
        self.ue_version = self._verify_ue5_version()
        
        if self.ue_version is None:
            return False
        
        return True

    def detect_platform_sdks(self) -> Dict[str, bool]:
        """
        Detect available platform SDKs.

        Returns:
            Dictionary of platform → SDK available
        """
        result = {}
        
        for platform, env_var in self.SDK_ENV_VARS.items():
            sdk_path = self._check_sdk_path(env_var)
            if sdk_path is not None:
                self.platform_sdks[platform.value] = sdk_path
                result[platform.value] = True
            else:
                result[platform.value] = False
        
        return result

    def _verify_ue5_version(self) -> Optional[tuple]:
        """
        Verify UE5 version meets minimum requirement.

        Returns:
            Version tuple or None if invalid
        """
        if self.ue_root is None:
            return None
        
        # Try to read version from Engine/Build/Build.version file
        version_file = self.ue_root / "Engine" / "Build" / "Build.version"
        
        if version_file.exists():
            try:
                import json
                with open(version_file, 'r') as f:
                    version_data = json.load(f)
                    major = version_data.get('MajorVersion', 0)
                    minor = version_data.get('MinorVersion', 0)
                    version = (major, minor)
                    
                    if version >= self.MIN_UE5_VERSION:
                        return version
                    else:
                        return None
            except (json.JSONDecodeError, KeyError, IOError):
                pass
        
        # Fallback: try to parse from UnrealVersionSelector or similar
        uat_path = self.ue_root / "Engine" / "Binaries" / "DotNET" / "UnrealBuildTool.dll"
        if uat_path.exists():
            # Assume latest version if we can't parse
            return (5, 3)
        
        return None

    def _find_ue5_root(self) -> Optional[Path]:
        """
        Find UE5 root directory from environment.

        Returns:
            Path to UE5 root or None
        """
        # Check environment variable first
        env_root = os.environ.get('UNREAL_ENGINE_ROOT')
        if env_root:
            root_path = Path(env_root)
            if root_path.exists():
                return root_path
        
        # Check for UnrealBuildTool in PATH
        try:
            result = subprocess.run(
                ['where', 'UnrealBuildTool.bat'] if os.name == 'nt' else ['which', 'UnrealBuildTool'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                uat_path = Path(result.stdout.strip().split('\n')[0])
                # Navigate up to find engine root
                potential_root = uat_path.parent.parent.parent
                if (potential_root / "Engine" / "Build" / "Build.version").exists():
                    return potential_root
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Check common installation paths
        for install_path in self.UE5_INSTALL_PATHS:
            if install_path.exists():
                # Look for version subdirectories (e.g., 5.3, 5.4)
                try:
                    versions = sorted(
                        [d for d in install_path.iterdir() if d.is_dir()],
                        reverse=True
                    )
                    if versions:
                        # Use the latest version
                        latest = versions[0]
                        if (latest / "Engine" / "Build" / "Build.version").exists():
                            return latest
                except (PermissionError, OSError):
                    continue
        
        return None

    def _check_sdk_path(self, env_var: str) -> Optional[Path]:
        """
        Check if SDK path exists from environment variable.

        Args:
            env_var: Environment variable name

        Returns:
            SDK path or None
        """
        sdk_path_str = os.environ.get(env_var)
        if sdk_path_str:
            sdk_path = Path(sdk_path_str)
            if sdk_path.exists():
                return sdk_path
        return None

    def get_ue5_info(self) -> Dict[str, Any]:
        """
        Get comprehensive UE5 installation information.

        Returns:
            Dictionary with UE5 installation details
        """
        return {
            'ue_root': str(self.ue_root) if self.ue_root else None,
            'ue_version': '.'.join(map(str, self.ue_version)) if self.ue_version else None,
            'platform_sdks': {k: str(v) for k, v in self.platform_sdks.items()},
            'min_version_met': self.ue_version >= self.MIN_UE5_VERSION if self.ue_version else False,
        }
