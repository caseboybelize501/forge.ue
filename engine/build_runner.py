"""
Build Runner — Level 5 Engine Module

Invoke UHT → UBT, capture errors.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.build_result (L0-004)
- contracts.models.code_artifact (L0-003)
- engine.cpp_generator (L4-001)
- ai.test_agent (L1-002)
"""
from typing import List, Dict, Optional
from pathlib import Path
import subprocess
import re
from datetime import datetime

from contracts.models.game_brief import GameBrief
from contracts.models.build_result import CompileResult, TestResult, ErrorReport
from contracts.models.code_artifact import CppFile


class BuildRunner:
    """
    UE5 Build Runner.

    Executes build pipeline:
    - UnrealHeaderTool (UHT) dry-run
    - UnrealBuildTool (UBT) compile
    - Error parsing and reporting
    - Test execution

    Attributes:
        ue_root: Path to UE5 installation
        cpp_generator: C++ generator reference
        test_agent: Test agent reference
    """

    # UBT error pattern
    UBT_ERROR_PATTERN = re.compile(
        r'(?P<file>.*):(?P<line>\d+):\d+: error: (?P<message>.*)'
    )

    # UHT error pattern
    UHT_ERROR_PATTERN = re.compile(
        r'(?P<file>.*\.h)\((?P<line>\d+)\):\s*error:\s*(?P<message>.*)'
    )

    # Warning pattern
    WARNING_PATTERN = re.compile(
        r'(?P<file>.*):(?P<line>\d+):\d+: warning: (?P<message>.*)'
    )

    def __init__(self, ue_root: Path, cpp_generator=None, test_agent=None):
        """
        Initialize build runner.

        Args:
            ue_root: Path to UE5 installation
            cpp_generator: C++ generator reference
            test_agent: Test agent reference
        """
        self.ue_root = ue_root
        self.cpp_generator = cpp_generator
        self.test_agent = test_agent

    def run_uht(self, project_path: Path) -> CompileResult:
        """
        Run UnrealHeaderTool dry-run.

        Args:
            project_path: Path to UE5 project

        Returns:
            Compilation result
        """
        start_time = datetime.now()

        # Find UHT executable
        uht_exe = self.ue_root / "Engine" / "Binaries" / "DotNET" / "UnrealHeaderTool.exe"

        if not uht_exe.exists():
            # Try alternative path for newer UE5 versions
            uht_exe = self.ue_root / "Engine" / "Binaries" / "DotNET" / "UnrealHeaderTool.sh"

        if not uht_exe.exists():
            return CompileResult(
                success=False,
                errors=[ErrorReport(
                    file_path=str(project_path),
                    error_type="UHT_NOT_FOUND",
                    error_message=f"UnrealHeaderTool not found at {uht_exe}"
                )],
                duration_seconds=0.0,
                timestamp=start_time
            )

        # Find .uproject file
        uproject_files = list(project_path.glob("*.uproject"))
        if not uproject_files:
            return CompileResult(
                success=False,
                errors=[ErrorReport(
                    file_path=str(project_path),
                    error_type="UPROJECT_NOT_FOUND",
                    error_message="No .uproject file found in project directory"
                )],
                duration_seconds=0.0,
                timestamp=start_time
            )

        uproject = uproject_files[0]

        # Run UHT dry-run
        cmd = [
            str(uht_exe),
            "-dryrun",
            "-project=" + str(uproject),
            "-log"
        ]

        result = self._run_command(cmd, project_path)

        # Parse errors
        errors = self._parse_uht_errors(result.stderr)
        warnings = self._parse_warnings(result.stderr)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        return CompileResult(
            success=result.returncode == 0 and len(errors) == 0,
            errors=errors,
            warnings=warnings,
            duration_seconds=duration,
            timestamp=end_time
        )

    def run_ubt(self, project_path: Path, configuration: str = "Development") -> CompileResult:
        """
        Run UnrealBuildTool compile.

        Args:
            project_path: Path to UE5 project
            configuration: Build configuration (Development, Shipping, etc.)

        Returns:
            Compilation result
        """
        start_time = datetime.now()

        # Find UBT executable
        ubt_exe = self.ue_root / "Engine" / "Binaries" / "DotNET" / "UnrealBuildTool.exe"

        if not ubt_exe.exists():
            return CompileResult(
                success=False,
                errors=[ErrorReport(
                    file_path=str(project_path),
                    error_type="UBT_NOT_FOUND",
                    error_message=f"UnrealBuildTool not found at {ubt_exe}"
                )],
                duration_seconds=0.0,
                timestamp=start_time
            )

        # Find .uproject file
        uproject_files = list(project_path.glob("*.uproject"))
        if not uproject_files:
            return CompileResult(
                success=False,
                errors=[ErrorReport(
                    file_path=str(project_path),
                    error_type="UPROJECT_NOT_FOUND",
                    error_message="No .uproject file found"
                )],
                duration_seconds=0.0,
                timestamp=start_time
            )

        uproject = uproject_files[0]
        project_name = uproject.stem

        # Run UBT
        cmd = [
            str(ubt_exe),
            "-project=" + str(uproject),
            f"{project_name}Editor",
            "Win64",
            configuration,
            "-waitmutex",
            "-compile",
            "-log"
        ]

        result = self._run_command(cmd, project_path)

        # Parse errors
        errors = self._parse_ubt_errors(result.stderr)
        warnings = self._parse_warnings(result.stderr)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        return CompileResult(
            success=result.returncode == 0 and len(errors) == 0,
            errors=errors,
            warnings=warnings,
            duration_seconds=duration,
            timestamp=end_time
        )

    def parse_ubt_errors(self, stderr: str) -> List[ErrorReport]:
        """
        Parse UBT stderr into structured errors.

        Args:
            stderr: UBT standard error output

        Returns:
            List of error reports
        """
        return self._parse_ubt_errors(stderr)

    def _parse_ubt_errors(self, stderr: str) -> List[ErrorReport]:
        """
        Parse UBT error output.

        Args:
            stderr: Error output

        Returns:
            List of error reports
        """
        errors = []

        for match in self.UBT_ERROR_PATTERN.finditer(stderr):
            errors.append(ErrorReport(
                file_path=match.group('file').strip(),
                line_number=int(match.group('line')),
                error_type="UBT_ERROR",
                error_message=match.group('message').strip(),
                suggestion=self._generate_suggestion(match.group('message'))
            ))

        return errors

    def _parse_uht_errors(self, stderr: str) -> List[ErrorReport]:
        """
        Parse UHT error output.

        Args:
            stderr: Error output

        Returns:
            List of error reports
        """
        errors = []

        for match in self.UHT_ERROR_PATTERN.finditer(stderr):
            errors.append(ErrorReport(
                file_path=match.group('file').strip(),
                line_number=int(match.group('line')),
                error_type="UHT_ERROR",
                error_message=match.group('message').strip(),
                suggestion=self._generate_suggestion(match.group('message'))
            ))

        return errors

    def _parse_warnings(self, stderr: str) -> List[str]:
        """
        Parse warnings from output.

        Args:
            stderr: Output with warnings

        Returns:
            List of warning messages
        """
        warnings = []

        for match in self.WARNING_PATTERN.finditer(stderr):
            warnings.append(
                f"{match.group('file')}:{match.group('line')}: {match.group('message')}"
            )

        return warnings

    def _generate_suggestion(self, error_message: str) -> Optional[str]:
        """
        Generate fix suggestion based on error type.

        Args:
            error_message: Error message

        Returns:
            Suggestion string or None
        """
        error_lower = error_message.lower()

        if "generated_body" in error_lower:
            return "Add GENERATED_BODY() macro to class definition"
        elif "uclass" in error_lower:
            return "Ensure UCLASS() macro is present before class declaration"
        elif "uproperty" in error_lower:
            return "Add UPROPERTY() macro with appropriate specifiers"
        elif "ufunction" in error_lower:
            return "Add UFUNCTION() macro before function declaration"
        elif "include" in error_lower or "cannot open file" in error_lower:
            return "Check include paths and file existence"
        elif "syntax" in error_lower:
            return "Check for missing semicolons or braces"
        elif "undefined" in error_lower:
            return "Ensure all symbols are properly defined and included"

        return None

    def run_tests(self, project_path: Path) -> TestResult:
        """
        Run UE5 Automation Tests.

        Args:
            project_path: Path to UE5 project

        Returns:
            Test result
        """
        start_time = datetime.now()

        # Find UE5 editor for test execution
        ue5_exe = self.ue_root / "Engine" / "Binaries" / "Win64" / "UnrealEditor-Cmd.exe"

        if not ue5_exe.exists():
            return TestResult(
                success=False,
                passed_tests=0,
                failed_tests=0,
                skipped_tests=0,
                details=[{"error": "UE5 Editor not found"}],
                duration_seconds=0.0,
                timestamp=start_time
            )

        # Find .uproject file
        uproject_files = list(project_path.glob("*.uproject"))
        if not uproject_files:
            return TestResult(
                success=False,
                passed_tests=0,
                failed_tests=0,
                skipped_tests=0,
                details=[{"error": "No .uproject file found"}],
                duration_seconds=0.0,
                timestamp=start_time
            )

        uproject = uproject_files[0]

        # Run tests
        cmd = [
            str(ue5_exe),
            str(uproject),
            "-run=automationtest",
            "-testexit=AllTests",
            "-unattended",
            "-nopause"
        ]

        result = self._run_command(cmd, project_path)

        # Parse test output
        test_result = self._parse_test_output(result.stdout, result.stderr)
        test_result.timestamp = datetime.now()
        test_result.duration_seconds = (test_result.timestamp - start_time).total_seconds()

        return test_result

    def _parse_test_output(self, stdout: str, stderr: str) -> TestResult:
        """
        Parse test output into structured result.

        Args:
            stdout: Standard output
            stderr: Standard error

        Returns:
            Test result
        """
        passed = 0
        failed = 0
        skipped = 0
        details = []

        # Parse test results
        for line in stdout.split('\n'):
            if 'PASSED' in line:
                passed += 1
                details.append({"status": "PASSED", "line": line.strip()})
            elif 'FAILED' in line:
                failed += 1
                details.append({"status": "FAILED", "line": line.strip()})
            elif 'SKIPPED' in line:
                skipped += 1
                details.append({"status": "SKIPPED", "line": line.strip()})

        return TestResult(
            success=failed == 0,
            passed_tests=passed,
            failed_tests=failed,
            skipped_tests=skipped,
            details=details,
            duration_seconds=0.0,
            timestamp=datetime.now()
        )

    def _run_command(self, cmd: List[str], cwd: Path) -> subprocess.CompletedProcess:
        """
        Run shell command and capture output.

        Args:
            cmd: Command and arguments
            cwd: Working directory

        Returns:
            Completed process
        """
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=1800  # 30 minute timeout
            )
            return result
        except subprocess.TimeoutExpired:
            # Return error result for timeout
            return subprocess.CompletedProcess(
                args=cmd,
                returncode=-1,
                stdout="",
                stderr="Build command timed out after 30 minutes"
            )
        except Exception as e:
            return subprocess.CompletedProcess(
                args=cmd,
                returncode=-1,
                stdout="",
                stderr=f"Build command failed: {str(e)}"
            )

    def build_full(self, project_path: Path, configuration: str = "Development") -> Dict[str, CompileResult]:
        """
        Run full build pipeline (UHT → UBT).

        Args:
            project_path: Path to UE5 project
            configuration: Build configuration

        Returns:
            Dictionary with UHT and UBT results
        """
        results = {}

        # Run UHT first
        results['uht'] = self.run_uht(project_path)

        # Only run UBT if UHT passed
        if results['uht'].success:
            results['ubt'] = self.run_ubt(project_path, configuration)
        else:
            results['ubt'] = CompileResult(
                success=False,
                errors=[ErrorReport(
                    file_path="",
                    error_type="SKIPPED",
                    error_message="UBT skipped due to UHT failures"
                )],
                duration_seconds=0.0,
                timestamp=datetime.now()
            )

        return results
