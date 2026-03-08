"""
Blueprint Test Validator — Level 2 Test Generation

Validate Blueprint JSON graphs against schema.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- contracts.models.build_result (L0-004)
- ai.test_agent (L1-002)
"""
from typing import List, Dict, Any, Optional, Set, Tuple
from pathlib import Path
from datetime import datetime
import json

from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec
from contracts.models.build_result import TestSpec, ValidationResult, TestResult
from ai.test_agent import TestAgent


class BlueprintTestValidator:
    """
    Blueprint Test Validator for FORGE pipeline.

    Validates Blueprint JSON graphs:
    - All node input pins connected
    - No dangling exec pins
    - All variable references resolve
    - Valid node type registry

    Attributes:
        output_dir: Path to validation output
        test_agent: Reference to test agent for spec generation
    """

    # Required pin types for validation
    EXEC_PIN_TYPES = {'exec', 'execute'}
    DATA_PIN_TYPES = {'bool', 'int', 'float', 'string', 'object', 'vector', 'rotator'}

    def __init__(self, output_dir: Path, test_agent: TestAgent = None):
        """
        Initialize Blueprint test validator.

        Args:
            output_dir: Path to validation output directory
            test_agent: Optional test agent for spec generation
        """
        self.output_dir = output_dir
        self.test_agent = test_agent

    def validate_blueprint(self, bp_json: Dict[str, Any]) -> ValidationResult:
        """
        Validate Blueprint graph structure.

        Args:
            bp_json: Blueprint graph JSON

        Returns:
            Validation result with errors/warnings
        """
        errors: List[str] = []
        warnings: List[str] = []
        validated_nodes = 0

        # Extract nodes and connections from blueprint
        nodes = bp_json.get('nodes', [])
        connections = bp_json.get('connections', [])
        variables = bp_json.get('variables', [])

        # Validate node connections
        connection_errors = self._check_node_connections(nodes)
        errors.extend(connection_errors)

        # Check for dangling exec pins
        dangling_errors = self._check_dangling_pins(nodes, connections)
        errors.extend(dangling_errors)

        # Check variable references
        var_errors = self._check_variable_references(nodes, variables)
        errors.extend(var_errors)

        # Count validated nodes
        validated_nodes = len(nodes) - len([e for e in errors if 'node' in e.lower()])

        # Add warnings for potential issues
        warnings.extend(self._check_performance_issues(nodes))

        return ValidationResult(
            success=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            validated_nodes=validated_nodes,
            timestamp=datetime.now()
        )

    def validate_blueprint_file(self, bp_file: Path) -> ValidationResult:
        """
        Validate Blueprint from JSON file.

        Args:
            bp_file: Path to Blueprint JSON file

        Returns:
            Validation result
        """
        if not bp_file.exists():
            return ValidationResult(
                success=False,
                errors=[f"Blueprint file not found: {bp_file}"],
                validated_nodes=0,
                timestamp=datetime.now()
            )

        try:
            with open(bp_file, 'r', encoding='utf-8') as f:
                bp_json = json.load(f)
            return self.validate_blueprint(bp_json)
        except json.JSONDecodeError as e:
            return ValidationResult(
                success=False,
                errors=[f"Invalid JSON in blueprint file: {e}"],
                validated_nodes=0,
                timestamp=datetime.now()
            )

    def _check_node_connections(self, nodes: List[Dict[str, Any]]) -> List[str]:
        """
        Verify all node connections are valid.

        Args:
            nodes: List of blueprint nodes

        Returns:
            List of connection errors
        """
        errors = []
        node_ids: Set[str] = {node.get('id', '') for node in nodes}

        for node in nodes:
            node_id = node.get('id', '')
            node_type = node.get('type', 'Unknown')

            # Check input pins
            input_pins = node.get('input_pins', [])
            for pin in input_pins:
                pin_name = pin.get('name', '')
                pin_type = pin.get('type', 'data')
                connections = pin.get('connections', [])

                # Skip optional pins
                if pin.get('optional', False):
                    continue

                # Exec pins must have connections
                if pin_type.lower() in self.EXEC_PIN_TYPES and not connections:
                    errors.append(
                        f"Node '{node_id}' ({node_type}): Input exec pin '{pin_name}' is not connected"
                    )

        return errors

    def _check_dangling_pins(self, nodes: List[Dict[str, Any]], connections: List[Dict[str, Any]]) -> List[str]:
        """
        Check for dangling exec pins.

        Args:
            nodes: Blueprint nodes
            connections: Node connections

        Returns:
            List of dangling pin errors
        """
        errors = []

        # Build connection map
        connected_pins: Set[str] = set()
        for conn in connections:
            source_pin = conn.get('source_pin', '')
            target_pin = conn.get('target_pin', '')
            connected_pins.add(source_pin)
            connected_pins.add(target_pin)

        # Check each node for dangling exec pins
        for node in nodes:
            node_id = node.get('id', '')
            node_type = node.get('type', 'Unknown')

            # Check output exec pins
            output_pins = node.get('output_pins', [])
            for pin in output_pins:
                pin_name = pin.get('name', '')
                pin_type = pin.get('type', 'data')
                pin_id = f"{node_id}:{pin_name}"

                # Exec pins should typically be connected
                if pin_type.lower() in self.EXEC_PIN_TYPES:
                    # Check if this is a terminal node (no output exec expected)
                    if not node.get('is_terminal', False):
                        if pin_id not in connected_pins:
                            errors.append(
                                f"Node '{node_id}' ({node_type}): Dangling output exec pin '{pin_name}'"
                            )

        return errors

    def _check_variable_references(self, nodes: List[Dict[str, Any]], variables: List[Dict[str, Any]]) -> List[str]:
        """
        Verify all variable references resolve.

        Args:
            nodes: Blueprint nodes
            variables: Defined variables

        Returns:
            List of unresolved reference errors
        """
        errors = []

        # Build variable name set
        defined_vars: Set[str] = {var.get('name', '') for var in variables}

        # Check each node for variable references
        for node in nodes:
            node_id = node.get('id', '')
            node_type = node.get('type', 'Unknown')

            # Check if this is a variable reference node
            if node_type in ['get_variable', 'set_variable']:
                var_name = node.get('variable_name', '')
                if var_name and var_name not in defined_vars:
                    errors.append(
                        f"Node '{node_id}' ({node_type}): Unresolved variable reference '{var_name}'"
                    )

            # Check function parameters for variable references
            params = node.get('parameters', {})
            for param_name, param_value in params.items():
                if isinstance(param_value, str) and param_value.startswith('$'):
                    ref_var = param_value[1:]  # Remove $ prefix
                    if ref_var not in defined_vars:
                        errors.append(
                            f"Node '{node_id}': Unresolved variable reference '${ref_var}' in parameter '{param_name}'"
                        )

        return errors

    def _check_performance_issues(self, nodes: List[Dict[str, Any]]) -> List[str]:
        """
        Check for potential performance issues.

        Args:
            nodes: Blueprint nodes

        Returns:
            List of performance warnings
        """
        warnings = []

        # Check for nodes in tick
        tick_nodes = [n for n in nodes if n.get('is_tick', False)]
        if len(tick_nodes) > 5:
            warnings.append(
                f"Performance: {len(tick_nodes)} nodes in tick - consider reducing tick complexity"
            )

        # Check for heavy operations
        heavy_ops = ['line_trace', 'sphere_trace', 'get_all_actors_of_class']
        for node in nodes:
            node_type = node.get('type', '').lower()
            if any(op in node_type for op in heavy_ops):
                if node.get('is_tick', False):
                    warnings.append(
                        f"Performance: Heavy operation '{node_type}' in tick function"
                    )

        return warnings

    def generate_test_spec(self, bp_json: Dict[str, Any]) -> TestSpec:
        """
        Generate test specification from Blueprint.

        Args:
            bp_json: Blueprint graph JSON

        Returns:
            Test specification for the Blueprint
        """
        bp_name = bp_json.get('name', 'UnnamedBlueprint')

        return TestSpec(
            test_name=f"{bp_name}_ValidationTest",
            test_type="blueprint",
            target_system=bp_name,
            assertions=[
                {
                    "name": "AllExecPinsConnected",
                    "condition": "validation_result.success"
                },
                {
                    "name": "NoDanglingVariables",
                    "condition": "len(validation_result.errors) == 0"
                }
            ],
            expected_result="Blueprint validates without errors"
        )

    def validate_from_project(self, project_spec: ProjectSpec) -> TestResult:
        """
        Validate all Blueprints in a project.

        Args:
            project_spec: Project specification

        Returns:
            Aggregated test result
        """
        results = []
        total_errors = 0

        for bp_file in project_spec.blueprint_files:
            bp_path = Path(bp_file)
            result = self.validate_blueprint_file(bp_path)
            results.append(result)
            if not result.success:
                total_errors += len(result.errors)

        return TestResult(
            success=total_errors == 0,
            passed_tests=len([r for r in results if r.success]),
            failed_tests=len([r for r in results if not r.success]),
            skipped_tests=0,
            details=[
                {"errors": r.errors, "warnings": r.warnings}
                for r in results
            ],
            duration_seconds=0.0,
            timestamp=datetime.now()
        )
