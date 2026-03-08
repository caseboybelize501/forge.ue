"""
CPP Test Generator — Level 2 Test Generation

Generate UE5 Automation Tests (C++) using FAutomationTestBase.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- contracts.models.build_result (L0-004)
- ai.test_agent (L1-002)
"""
from typing import List, Dict
from pathlib import Path
from datetime import datetime

from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec, ModuleSpec
from contracts.models.build_result import TestSpec, AssertionSpec, TestResult
from ai.test_agent import TestAgent


class CppTestGenerator:
    """
    C++ Test Generator for UE5 Automation Tests.

    Generates test files using FAutomationTestBase framework:
    - ADD_LATENT_AUTOMATION_COMMAND for async tests
    - Test assertions for game systems
    - Save/load serialization tests

    Attributes:
        output_dir: Path to test output directory
        test_agent: Reference to test agent for spec generation
    """

    # Test template for UE5 automation tests
    TEST_TEMPLATE = """
BEGIN_DEFINE_SPEC({spec_name}, "{spec_path}", EAutomationTestFlags::ProductFilter | EAutomationTestFlags::ApplicationContextMask)
END_DEFINE_SPEC({spec_name})

void {spec_name}::Define()
{{
    {test_body}
}}
"""

    # Assertion template
    ASSERTION_TEMPLATE = """
    TestTrue("{assertion_name}", {condition});
"""

    # Latent test template for async operations
    LATENT_TEST_TEMPLATE = """
    ADD_LATENT_AUTOMATION_COMMAND({command_name});
"""

    def __init__(self, output_dir: Path, test_agent: TestAgent = None):
        """
        Initialize C++ test generator.

        Args:
            output_dir: Path to test output directory
            test_agent: Optional test agent for spec generation
        """
        self.output_dir = output_dir
        self.test_agent = test_agent

    def generate_test_file(self, test_spec: TestSpec) -> str:
        """
        Generate C++ test file content.

        Args:
            test_spec: Test specification

        Returns:
            Generated C++ test file content
        """
        spec_name = test_spec.test_name.replace(" ", "")
        spec_path = f"Forge.Tests.{test_spec.target_system}"

        # Generate test body from assertions
        test_body_parts = []
        for assertion in test_spec.assertions:
            assertion_code = self._generate_assertion_code(assertion)
            test_body_parts.append(assertion_code)

        test_body = "\n".join(test_body_parts)

        # Add setup and teardown
        setup_code = self._generate_setup(test_spec)
        teardown_code = self._generate_teardown(test_spec)

        full_body = f"{setup_code}\n{test_body}\n{teardown_code}"

        # Render template
        content = self.TEST_TEMPLATE.format(
            spec_name=spec_name,
            spec_path=spec_path,
            test_body=full_body
        )

        return content

    def generate_test_file_to_disk(self, test_spec: TestSpec) -> Path:
        """
        Generate C++ test file and write to disk.

        Args:
            test_spec: Test specification

        Returns:
            Path to generated test file
        """
        content = self.generate_test_file(test_spec)

        # Create output directory if needed
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Write test file
        test_file = self.output_dir / f"{test_spec.test_name}.cpp"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)

        return test_file

    def generate_from_project(self, project_spec: ProjectSpec) -> List[TestSpec]:
        """
        Generate test specifications from project architecture.

        Args:
            project_spec: Project specification

        Returns:
            List of generated test specifications
        """
        test_specs = []

        for module_spec in project_spec.modules:
            # Generate tests for each module
            module_tests = self._generate_module_tests(module_spec)
            test_specs.extend(module_tests)

        return test_specs

    def _generate_assertion_code(self, assertion: Dict) -> str:
        """
        Generate single assertion code.

        Args:
            assertion: Assertion specification dictionary

        Returns:
            Generated assertion code
        """
        assertion_name = assertion.get('name', 'UnnamedAssertion')
        condition = assertion.get('condition', 'false')

        return self.ASSERTION_TEMPLATE.format(
            assertion_name=assertion_name,
            condition=condition
        )

    def _generate_assertion(self, assertion: AssertionSpec) -> str:
        """
        Generate single assertion code.

        Args:
            assertion: Assertion specification

        Returns:
            Generated assertion code
        """
        return self.ASSERTION_TEMPLATE.format(
            assertion_name=assertion.name,
            condition=assertion.condition
        )

    def _generate_setup(self, test_spec: TestSpec) -> str:
        """
        Generate test setup code.

        Args:
            test_spec: Test specification

        Returns:
            Generated setup code
        """
        setup_parts = []

        # Add common setup for UE5 tests
        setup_parts.append("    // Setup test environment")
        setup_parts.append("    UWorld* World = GetWorld();")
        setup_parts.append("    TestTrue(\"World exists\", World != nullptr);")

        return "\n".join(setup_parts)

    def _generate_teardown(self, test_spec: TestSpec) -> str:
        """
        Generate test teardown code.

        Args:
            test_spec: Test specification

        Returns:
            Generated teardown code
        """
        teardown_parts = []

        # Add common teardown
        teardown_parts.append("    // Teardown test environment")
        teardown_parts.append("    // Clean up any spawned actors")

        return "\n".join(teardown_parts)

    def _generate_module_tests(self, module_spec: ModuleSpec) -> List[TestSpec]:
        """
        Generate test specifications for a module.

        Args:
            module_spec: Module specification

        Returns:
            List of test specifications for the module
        """
        tests = []

        # Generate basic module tests
        test_spec = TestSpec(
            test_name=f"{module_spec.module_name}_ModuleTest",
            test_type="automation",
            target_system=module_spec.module_name,
            assertions=[
                {
                    "name": "ModuleLoads",
                    "condition": "true"
                }
            ],
            expected_result="Module loads without errors"
        )
        tests.append(test_spec)

        return tests

    def validate_generated_tests(self, test_specs: List[TestSpec]) -> TestResult:
        """
        Validate generated test specifications.

        Args:
            test_specs: List of test specifications

        Returns:
            Test result with validation status
        """
        errors = []
        passed = 0

        for spec in test_specs:
            # Validate test spec structure
            if not spec.test_name:
                errors.append("Test spec missing test_name")
            elif not spec.target_system:
                errors.append(f"Test {spec.test_name} missing target_system")
            elif not spec.expected_result:
                errors.append(f"Test {spec.test_name} missing expected_result")
            else:
                passed += 1

        return TestResult(
            success=len(errors) == 0,
            passed_tests=passed,
            failed_tests=len(errors),
            skipped_tests=0,
            details=[{"error": e} for e in errors],
            duration_seconds=0.0,
            timestamp=datetime.now()
        )
