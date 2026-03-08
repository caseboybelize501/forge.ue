"""
Test Harness — Level 2 Test Generation

Orchestrate UE5 test runner execution.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- contracts.models.build_result (L0-004)
- ai.test_agent (L1-002)
"""
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
import subprocess
import re
import json

from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec
from contracts.models.build_result import TestSpec, TestResult
from ai.test_agent import TestAgent


class TestHarness:
    """
    Test Harness for UE5 Automation Test execution.

    Orchestrates test runner:
    - Launches UE5 in test mode
    - Captures test output
    - Aggregates results
    - Generates reports

    Attributes:
        ue_root: Path to Unreal Engine installation
        output_dir: Path to test results output
        test_agent: Reference to test agent for spec generation
    """

    # UE5 test runner command template
    UE5_TEST_COMMAND = (
        '"{ue5_exe}" "{project_path}" '
        '-run=automationworker '
        '-testexit=AllTests '
        '-outputlog="{log_path}" '
        '-unattended '
        '-nopause'
    )

    # Test output parsing patterns
    TEST_RESULT_PATTERN = re.compile(
        r'(?P<test_name>[\w_]+):\s*(?P<status>PASSED|FAILED|SKIPPED)'
    )
    TEST_SUMMARY_PATTERN = re.compile(
        r'Test Summary:\s*(?P<passed>\d+)\s*passed,\s*(?P<failed>\d+)\s*failed,\s*(?P<skipped>\d+)\s*skipped'
    )

    def __init__(self, ue_root: Path, output_dir: Path, test_agent: TestAgent = None):
        """
        Initialize test harness.

        Args:
            ue_root: Path to UE5 installation
            output_dir: Path to test results output
            test_agent: Optional test agent for spec generation
        """
        self.ue_root = ue_root
        self.output_dir = output_dir
        self.test_agent = test_agent

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_tests(self, test_specs: List[TestSpec], project_path: Path) -> TestResult:
        """
        Execute all tests and aggregate results.

        Args:
            test_specs: List of test specifications
            project_path: Path to UE5 project

        Returns:
            Aggregated test result
        """
        # Generate test log path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = self.output_dir / f"test_results_{timestamp}.log"

        # Run UE5 automation
        result = self._run_ue5_automation(project_path, log_path)

        # Parse test output
        test_result = self._parse_test_output(result, log_path)

        # Generate report
        report = self._generate_report(test_result)

        # Save report
        report_path = self.output_dir / f"test_report_{timestamp}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return test_result

    def run_single_test(self, test_spec: TestSpec, project_path: Path) -> TestResult:
        """
        Run a single test specification.

        Args:
            test_spec: Test specification
            project_path: Path to UE5 project

        Returns:
            Test result for the single test
        """
        # Generate test file
        from ai.test_generation.cpp_test_generator import CppTestGenerator

        generator = CppTestGenerator(self.output_dir)
        test_file = generator.generate_test_file_to_disk(test_spec)

        # Run tests
        return self.run_tests([test_spec], project_path)

    def _run_ue5_automation(self, project_path: Path, log_path: Path) -> subprocess.CompletedProcess:
        """
        Run UE5 Automation Test runner.

        Args:
            project_path: Path to UE5 project
            log_path: Path to output log file

        Returns:
            Completed process with output
        """
        # Find UE5 executable
        ue5_exe = self.ue_root / "Engine" / "Binaries" / "Win64" / "UnrealEditor-Cmd.exe"

        if not ue5_exe.exists():
            # Return error result
            return subprocess.CompletedProcess(
                args=[],
                returncode=1,
                stdout="",
                stderr=f"UE5 executable not found at {ue5_exe}"
            )

        # Build command
        command = self.UE5_TEST_COMMAND.format(
            ue5_exe=str(ue5_exe),
            project_path=str(project_path),
            log_path=str(log_path)
        )

        # Run command
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            return result
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess(
                args=[command],
                returncode=-1,
                stdout="",
                stderr="Test execution timed out after 1 hour"
            )
        except Exception as e:
            return subprocess.CompletedProcess(
                args=[command],
                returncode=-1,
                stdout="",
                stderr=f"Test execution failed: {e}"
            )

    def _parse_test_output(self, process_result: subprocess.CompletedProcess, log_path: Path) -> TestResult:
        """
        Parse UE5 test output into structured result.

        Args:
            process_result: Completed process from test runner
            log_path: Path to log file

        Returns:
            Parsed test result
        """
        errors = []
        passed = 0
        failed = 0
        skipped = 0
        details = []

        # Try to read log file
        if log_path.exists():
            try:
                with open(log_path, 'r', encoding='utf-8') as f:
                    log_content = f.read()

                # Parse test results from log
                for match in self.TEST_RESULT_PATTERN.finditer(log_content):
                    test_name = match.group('test_name')
                    status = match.group('status')

                    if status == 'PASSED':
                        passed += 1
                    elif status == 'FAILED':
                        failed += 1
                        errors.append(f"Test failed: {test_name}")
                    else:
                        skipped += 1

                    details.append({
                        "test_name": test_name,
                        "status": status
                    })

                # Try to parse summary
                summary_match = self.TEST_SUMMARY_PATTERN.search(log_content)
                if summary_match:
                    passed = int(summary_match.group('passed'))
                    failed = int(summary_match.group('failed'))
                    skipped = int(summary_match.group('skipped'))

            except (IOError, OSError) as e:
                errors.append(f"Failed to read log file: {e}")
        else:
            # Use process result
            if process_result.returncode != 0:
                errors.append(process_result.stderr or "Unknown error")

        return TestResult(
            success=failed == 0 and len(errors) == 0,
            passed_tests=passed,
            failed_tests=failed,
            skipped_tests=skipped,
            details=details,
            duration_seconds=self._parse_duration(log_path),
            timestamp=datetime.now()
        )

    def _parse_duration(self, log_path: Path) -> float:
        """
        Parse test duration from log file.

        Args:
            log_path: Path to log file

        Returns:
            Duration in seconds
        """
        if not log_path.exists():
            return 0.0

        duration_pattern = re.compile(r'Total time:\s*(?P<seconds>[\d.]+)\s*seconds')

        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
                match = duration_pattern.search(content)
                if match:
                    return float(match.group('seconds'))
        except (IOError, OSError, ValueError):
            pass

        return 0.0

    def _generate_report(self, result: TestResult) -> str:
        """
        Generate human-readable test report.

        Args:
            result: Test result

        Returns:
            Formatted report string
        """
        lines = [
            "=" * 60,
            "FORGE TEST REPORT",
            "=" * 60,
            f"Timestamp: {result.timestamp}",
            f"Status: {'PASSED' if result.success else 'FAILED'}",
            "",
            "SUMMARY",
            "-" * 40,
            f"  Passed:  {result.passed_tests}",
            f"  Failed:  {result.failed_tests}",
            f"  Skipped: {result.skipped_tests}",
            f"  Duration: {result.duration_seconds:.2f}s",
            "",
        ]

        if result.details:
            lines.append("TEST DETAILS")
            lines.append("-" * 40)
            for detail in result.details:
                test_name = detail.get('test_name', 'Unknown')
                status = detail.get('status', 'Unknown')
                status_icon = "✓" if status == 'PASSED' else "✗" if status == 'FAILED' else "○"
                lines.append(f"  {status_icon} {test_name}: {status}")
            lines.append("")

        if result.failed_tests > 0:
            lines.append("FAILURES")
            lines.append("-" * 40)
            for i, detail in enumerate(result.details):
                if detail.get('status') == 'FAILED':
                    lines.append(f"  {i + 1}. {detail.get('test_name', 'Unknown')}")
            lines.append("")

        lines.append("=" * 60)

        return "\n".join(lines)

    def run_from_project(self, project_spec: ProjectSpec) -> TestResult:
        """
        Run all tests for a project specification.

        Args:
            project_spec: Project specification

        Returns:
            Aggregated test result
        """
        # Generate test specs from project
        test_specs = self._generate_test_specs(project_spec)

        # Create dummy project path for now
        project_path = Path(project_spec.project_name)

        return self.run_tests(test_specs, project_path)

    def _generate_test_specs(self, project_spec: ProjectSpec) -> List[TestSpec]:
        """
        Generate test specifications from project.

        Args:
            project_spec: Project specification

        Returns:
            List of test specifications
        """
        test_specs = []

        # Generate module tests
        for module in project_spec.modules:
            test_specs.append(TestSpec(
                test_name=f"{module.module_name}_Test",
                test_type="automation",
                target_system=module.module_name,
                assertions=[
                    {"name": "ModuleCompiles", "condition": "true"},
                    {"name": "ModuleLoads", "condition": "true"}
                ],
                expected_result="Module compiles and loads successfully"
            ))

        return test_specs
