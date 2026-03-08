"""
Test Agent — Level 1 Core Agent

Generates test specifications per generated system.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.build_result (L0-004)
"""
from typing import List, Dict
from pathlib import Path

from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec, ModuleSpec
from contracts.models.build_result import TestSpec, TestResult


class TestAgent:
    """
    Test Agent for FORGE pipeline.

    Generates comprehensive test specifications:
    - UE5 Automation Tests (C++)
    - Blueprint Validation Specs (JSON)
    - Platform Guard Tests (Python)

    Attributes:
        output_dir: Path to test output directory
    """

    def __init__(self, output_dir: Path):
        """
        Initialize test agent.

        Args:
            output_dir: Path to test output directory
        """
        self.output_dir = output_dir
        self._test_specs: List[TestSpec] = []

    def generate_test_specs(self, project_spec: ProjectSpec) -> List[TestSpec]:
        """
        Create test specs for all systems in project.

        Args:
            project_spec: Project architecture specification

        Returns:
            List of test specifications
        """
        self._test_specs = []
        
        # Generate C++ automation test specs
        cpp_specs = self._generate_cpp_test_specs(project_spec)
        self._test_specs.extend(cpp_specs)
        
        # Generate Blueprint validation specs
        bp_specs = self._generate_blueprint_test_specs(project_spec)
        self._test_specs.extend(bp_specs)
        
        # Generate platform guard validation specs
        platform_specs = self._generate_platform_guard_specs(project_spec)
        self._test_specs.extend(platform_specs)
        
        return self._test_specs

    def _generate_cpp_test_specs(self, project_spec: ProjectSpec) -> List[TestSpec]:
        """
        Generate C++ automation test specs.

        Args:
            project_spec: Project specification

        Returns:
            List of C++ test specs
        """
        specs = []
        
        for module in project_spec.modules:
            # Generate test spec for each module
            test_spec = TestSpec(
                test_name=f"{module.module_name}_ModuleTest",
                test_type="automation",
                target_system=module.module_name,
                assertions=[
                    {
                        "type": "module_loads",
                        "expected": True
                    },
                    {
                        "type": "classes_registered",
                        "expected": True
                    }
                ],
                expected_result=f"Module {module.module_name} loads and registers correctly"
            )
            specs.append(test_spec)
        
        return specs

    def _generate_blueprint_test_specs(self, project_spec: ProjectSpec) -> List[TestSpec]:
        """
        Generate Blueprint validation specs.

        Args:
            project_spec: Project specification

        Returns:
            List of Blueprint test specs
        """
        specs = []
        
        for module in project_spec.modules:
            # Generate BP test spec for each module with BP support
            test_spec = TestSpec(
                test_name=f"{module.module_name}_BPIntegrationTest",
                test_type="blueprint",
                target_system=module.module_name,
                assertions=[
                    {
                        "type": "bp_functions_exposed",
                        "expected": True
                    },
                    {
                        "type": "bp_events_registered",
                        "expected": True
                    }
                ],
                expected_result=f"Blueprint integration for {module.module_name} works correctly"
            )
            specs.append(test_spec)
        
        return specs

    def _generate_platform_guard_specs(self, project_spec: ProjectSpec) -> List[TestSpec]:
        """
        Generate platform guard validation specs.

        Args:
            project_spec: Project specification

        Returns:
            List of platform guard test specs
        """
        specs = []
        
        # Check if project has platform-specific modules
        for module in project_spec.modules:
            if module.platform_guards:
                for platform in module.platform_guards:
                    test_spec = TestSpec(
                        test_name=f"{module.module_name}_{platform}_GuardTest",
                        test_type="platform_guard",
                        target_system=module.module_name,
                        assertions=[
                            {
                                "type": "platform_guard_present",
                                "platform": platform,
                                "expected": True
                            }
                        ],
                        expected_result=f"Platform guards for {platform} are correctly applied"
                    )
                    specs.append(test_spec)
        
        return specs

    def save_test_specs(self, specs: List[TestSpec]) -> Path:
        """
        Save test specifications to output directory.

        Args:
            specs: List of test specifications to save

        Returns:
            Path to saved test specs file
        """
        import json
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert specs to serializable format
        specs_data = [spec.model_dump() for spec in specs]
        
        output_file = self.output_dir / "test_specs.json"
        with open(output_file, 'w') as f:
            json.dump(specs_data, f, indent=2)
        
        return output_file
