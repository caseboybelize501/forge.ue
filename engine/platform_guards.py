"""
Platform Guards — Level 4 Engine Module

Inject and validate platform guard macros.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.platform_spec (L0-006)
"""
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path
import re

from contracts.models.game_brief import Platform
from contracts.models.platform_spec import PlatformTarget, SDKStatus, PackageConfig


class PlatformGuards:
    """
    Platform Guard Manager.

    Handles platform-specific code guards:
    - Inject #if PLATFORM_* macros
    - Validate guard coverage
    - Detect unguarded SDK symbols

    Attributes:
        PLATFORM_GUARDS: Mapping of platform → guard macro
    """

    # Platform guard macro mapping
    PLATFORM_GUARDS = {
        "PS5": "#if PLATFORM_PS5",
        "XBOX": "#if PLATFORM_XBOXONE",
        "SWITCH": "#if PLATFORM_SWITCH",
        "ANDROID": "#if PLATFORM_ANDROID",
        "IOS": "#if PLATFORM_IOS",
        "MAC": "#if PLATFORM_MAC",
        "LINUX": "#if PLATFORM_LINUX",
        "WIN64": "#if PLATFORM_WINDOWS",
    }

    # Platform end guard
    PLATFORM_END = "#endif // PLATFORM_*"

    # SDK symbols that require platform guards
    SDK_SYMBOLS = {
        "PS5": [r"\bsce\b", r"\bSce\b", r"\bSCE\b"],
        "XBOX": [r"\bXbl\b", r"\bXBOX\b", r"\bxbox\b", r"\bIXbox\b"],
        "SWITCH": [r"\bnn\b", r"\bNX\b", r"\bSwitch\b"],
        "ANDROID": [r"\bandroid\b", r"\bAndroid\b", r"\bJNI\b"],
        "IOS": [r"\biOS\b", r"\bUIKit\b", r"\bNSObject\b"],
        "MAC": [r"\bCocoa\b", r"\bNSApplication\b"],
        "LINUX": [r"\bX11\b", r"\bWayland\b"],
    }

    # Platform-specific include patterns
    PLATFORM_INCLUDES = {
        "PS5": r"#include\s*[<\"]\s*sce",
        "XBOX": r"#include\s*[<\"]\s*xbox",
        "SWITCH": r"#include\s*[<\"]\s*nn/",
        "ANDROID": r"#include\s*[<\"]\s*android",
        "IOS": r"#include\s*[<\"]\s*UIKit",
    }

    def __init__(self):
        """Initialize platform guards manager."""
        self._compiled_patterns: Dict[str, List[re.Pattern]] = {}
        self._compile_patterns()

    def _compile_patterns(self) -> None:
        """Compile regex patterns for performance."""
        for platform, patterns in self.SDK_SYMBOLS.items():
            self._compiled_patterns[platform] = [
                re.compile(p) for p in patterns
            ]

    def wrap_code(self, code: str, platform: Platform) -> str:
        """
        Wrap code in platform guard macros.

        Args:
            code: Code to wrap
            platform: Target platform

        Returns:
            Guarded code
        """
        platform_upper = platform.value.upper()
        guard_macro = self.PLATFORM_GUARDS.get(platform_upper, f"#if PLATFORM_{platform_upper}")

        # Check if code is already guarded
        if self._is_already_guarded(code, platform_upper):
            return code

        # Wrap code
        guarded_code = f"""{guard_macro}
{code}
#endif // PLATFORM_{platform_upper}
"""
        return guarded_code

    def wrap_for_platforms(self, code: str, platforms: List[Platform]) -> str:
        """
        Wrap code for multiple platforms.

        Args:
            code: Code to wrap
            platforms: List of target platforms

        Returns:
            Guarded code for all platforms
        """
        if not platforms:
            return code

        if len(platforms) == 1:
            return self.wrap_code(code, platforms[0])

        # Multiple platforms - use OR condition
        platform_conditions = []
        for p in platforms:
            platform_upper = p.value.upper()
            if platform_upper in self.PLATFORM_GUARDS:
                platform_conditions.append(f"PLATFORM_{platform_upper}")

        if not platform_conditions:
            return code

        guard = " || ".join([f"({c})" for c in platform_conditions])
        guarded_code = f"""#if {guard}
{code}
#endif // {guard}
"""
        return guarded_code

    def validate_guards(self, file_content: str, file_path: str = "") -> List[str]:
        """
        Validate all platform-specific code is guarded.

        Args:
            file_content: File content to validate
            file_path: Optional file path for error messages

        Returns:
            List of guard violations
        """
        violations = []
        lines = file_content.split('\n')

        # Track current guard state
        active_guards: List[str] = []

        for line_num, line in enumerate(lines, 1):
            # Check for platform guard start
            for platform, guard in self.PLATFORM_GUARDS.items():
                if guard in line:
                    active_guards.append(platform)
                    break

            # Check for end guard
            if "#endif" in line and active_guards:
                active_guards.pop()

            # Check for SDK symbols
            for platform, patterns in self._compiled_patterns.items():
                for pattern in patterns:
                    if pattern.search(line):
                        # Check if guarded
                        if platform not in active_guards:
                            violation = (
                                f"{file_path}:{line_num}: "
                                f"Unguarded {platform} SDK symbol found: '{line.strip()}'"
                            )
                            violations.append(violation)

        return violations

    def _check_guard_coverage(self, content: str, line_num: int) -> bool:
        """
        Check if line is covered by platform guard.

        Args:
            content: File content
            line_num: Line number to check

        Returns:
            True if line is guarded
        """
        lines = content.split('\n')

        if line_num < 1 or line_num > len(lines):
            return False

        # Count guards before this line
        guard_depth = 0
        for i in range(line_num - 1):
            line = lines[i]
            if any(guard in line for guard in self.PLATFORM_GUARDS.values()):
                guard_depth += 1
            elif "#endif" in line and guard_depth > 0:
                guard_depth -= 1

        return guard_depth > 0

    def _find_sdk_symbols(self, content: str) -> List[Tuple[int, str, str]]:
        """
        Find SDK-specific symbols in content.

        Args:
            content: File content

        Returns:
            List of (line_num, symbol, platform) tuples
        """
        symbols = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            for platform, patterns in self._compiled_patterns.items():
                for pattern in patterns:
                    match = pattern.search(line)
                    if match:
                        symbols.append((line_num, match.group(0), platform))

        return symbols

    def _is_already_guarded(self, code: str, platform: str) -> bool:
        """
        Check if code is already guarded for a platform.

        Args:
            code: Code to check
            platform: Platform to check for

        Returns:
            True if already guarded
        """
        guard = self.PLATFORM_GUARDS.get(platform, f"#if PLATFORM_{platform}")
        return guard in code

    def inject_platform_checks(self, code: str, target_platforms: List[Platform]) -> str:
        """
        Inject platform availability checks into code.

        Args:
            code: Code to modify
            target_platforms: List of target platforms

        Returns:
            Modified code with platform checks
        """
        if not target_platforms:
            return code

        # Generate platform check function
        check_function = """
FORCEINLINE_DEBUGFUNCTION static bool IsPlatformSupported()
{
#if"""
        conditions = []
        for p in target_platforms:
            platform_upper = p.value.upper()
            conditions.append(f"PLATFORM_{platform_upper}")

        check_function += " || ".join(conditions)
        check_function += """
    return true;
#else
    return false;
#endif
}

"""
        # Inject at beginning of code
        return check_function + code

    def generate_platform_config(self, platforms: List[Platform]) -> Dict[str, Any]:
        """
        Generate platform configuration dictionary.

        Args:
            platforms: List of target platforms

        Returns:
            Platform configuration dictionary
        """
        config = {
            "platforms": [],
            "guards": {},
            "sdk_requirements": {}
        }

        for p in platforms:
            platform_upper = p.value.upper()
            guard = self.PLATFORM_GUARDS.get(platform_upper, f"PLATFORM_{platform_upper}")

            config["platforms"].append(p.value)
            config["guards"][p.value] = guard
            config["sdk_requirements"][p.value] = list(self.SDK_SYMBOLS.get(platform_upper, []))

        return config

    def get_supported_platforms(self) -> List[str]:
        """
        Get list of supported platforms.

        Returns:
            List of platform names
        """
        return list(self.PLATFORM_GUARDS.keys())

    def get_guard_macro(self, platform: Platform) -> str:
        """
        Get guard macro for a platform.

        Args:
            platform: Target platform

        Returns:
            Guard macro string
        """
        platform_upper = platform.value.upper()
        return self.PLATFORM_GUARDS.get(platform_upper, f"#if PLATFORM_{platform_upper}")

    def strip_guards(self, code: str) -> str:
        """
        Strip all platform guards from code.

        Args:
            code: Code to strip

        Returns:
            Code without guards
        """
        lines = code.split('\n')
        result = []
        guard_depth = 0

        for line in lines:
            if any(guard in line for guard in self.PLATFORM_GUARDS.values()):
                guard_depth += 1
            elif "#endif" in line:
                if guard_depth > 0:
                    guard_depth -= 1
            elif guard_depth == 0:
                result.append(line)

        return '\n'.join(result)
