"""
Blueprint Generator — Level 4 Engine Module

Generate Blueprint graphs as structured JSON.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- engine.project_scaffolder (L3-001)
"""
from typing import List, Dict, Optional, Any
from pathlib import Path
import json
import uuid

from contracts.models.game_brief import GameBrief
from contracts.models.project_spec import ProjectSpec, ModuleSpec
from contracts.models.code_artifact import BlueprintGraph, BlueprintNode


class BlueprintGenerator:
    """
    Blueprint Graph Generator.

    Generates Blueprint graphs as structured JSON:
    - Node graph with positions
    - Pin connections
    - Variable definitions
    - Event dispatchers

    Attributes:
        scaffolder: Project scaffolder reference
        output_dir: Blueprint output directory
    """

    # Blueprint node templates
    EVENT_BEGIN_PLAY = {
        "type": "K2Node_Event",
        "name": "EventBeginPlay",
        "function_name": "ReceiveBeginPlay",
        "inputs": [],
        "outputs": [{"name": "OutputExecPin", "type": "exec"}]
    }

    EVENT_TICK = {
        "type": "K2Node_Event",
        "name": "EventTick",
        "function_name": "ReceiveTick",
        "inputs": [
            {"name": "DeltaTime", "type": "float"}
        ],
        "outputs": [{"name": "OutputExecPin", "type": "exec"}]
    }

    def __init__(self, scaffolder: Optional['ProjectScaffolder'] = None):
        """
        Initialize Blueprint generator.

        Args:
            scaffolder: Project scaffolder reference
        """
        self.scaffolder = scaffolder
        self.output_dir: Optional[Path] = None

    def generate_blueprint(self, spec: ProjectSpec, system: str) -> BlueprintGraph:
        """
        Generate Blueprint graph for system.

        Args:
            spec: Project specification
            system: System name

        Returns:
            Generated Blueprint graph
        """
        # Generate unique graph ID
        graph_id = str(uuid.uuid4())

        # Generate nodes based on system type
        nodes = self._generate_nodes_for_system(system)

        # Generate connections
        connections = self._generate_connections(nodes)

        # Generate variables
        variables = self._generate_variables(system)

        # Create BlueprintGraph
        return BlueprintGraph(
            path=f"Content/Blueprints/{system}_BP",
            graph_name=f"{system}_BP",
            nodes=nodes,
            connections=connections,
            variables=variables,
            graph_id=graph_id
        )

    def generate_from_module(self, module: ModuleSpec) -> List[BlueprintGraph]:
        """
        Generate Blueprint graphs for a module.

        Args:
            module: Module specification

        Returns:
            List of generated Blueprint graphs
        """
        graphs = []

        # Generate BP for each module based on type
        if module.module_type.value in ["GameFramework", "GenreSystem"]:
            # Generate gameplay BP
            gameplay_bp = self.generate_blueprint(
                ProjectSpec(
                    project_id="TEMP",
                    project_name=module.module_name,
                    modules=[module],
                    platform_targets=["Win64"]
                ),
                f"{module.module_name}_Gameplay"
            )
            graphs.append(gameplay_bp)

        # Generate UI BP for UI modules
        if module.module_type.value == "UI":
            ui_bp = self.generate_blueprint(
                ProjectSpec(
                    project_id="TEMP",
                    project_name=module.module_name,
                    modules=[module],
                    platform_targets=["Win64"]
                ),
                f"{module.module_name}_Widget"
            )
            graphs.append(ui_bp)

        return graphs

    def save_blueprint(self, graph: BlueprintGraph, output_path: Path) -> Path:
        """
        Save Blueprint graph to JSON file.

        Args:
            graph: Blueprint graph to save
            output_path: Output directory

        Returns:
            Path to saved file
        """
        output_path.mkdir(parents=True, exist_ok=True)

        # Convert to dictionary
        bp_dict = {
            "graph_id": graph.graph_id,
            "graph_name": graph.graph_name,
            "nodes": [self._node_to_dict(node) for node in graph.nodes],
            "connections": graph.connections,
            "variables": graph.variables
        }

        # Write to file
        file_path = output_path / f"{graph.graph_name}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(bp_dict, f, indent=2)

        return file_path

    def _generate_nodes_for_system(self, system: str) -> List[BlueprintNode]:
        """
        Generate nodes for a specific system.

        Args:
            system: System name

        Returns:
            List of Blueprint nodes
        """
        nodes = []
        node_id = 0

        # Add Event BeginPlay
        nodes.append(BlueprintNode(
            node_id=f"node_{node_id}",
            node_type="K2Node_Event",
            node_name="EventBeginPlay",
            position={"x": 0, "y": 0},
            input_pins=[],
            output_pins=[{"name": "OutputExecPin", "type": "exec"}],
            properties={"EventName": "ReceiveBeginPlay"}
        ))
        node_id += 1

        # Add system-specific nodes
        if "Game" in system or "Gameplay" in system:
            # Add spawn node
            nodes.append(BlueprintNode(
                node_id=f"node_{node_id}",
                node_type="K2Node_CallFunction",
                node_name="SpawnActorFromClass",
                position={"x": 300, "y": 0},
                input_pins=[
                    {"name": "WorldContext", "type": "object"},
                    {"name": "Class", "type": "class"},
                    {"name": "SpawnTransform", "type": "transform"}
                ],
                output_pins=[
                    {"name": "ReturnValue", "type": "object"},
                    {"name": "OutputExecPin", "type": "exec"}
                ],
                properties={"FunctionName": "SpawnActorFromClass"}
            ))
            node_id += 1

        if "Widget" in system or "UI" in system:
            # Add Create Widget node
            nodes.append(BlueprintNode(
                node_id=f"node_{node_id}",
                node_type="K2Node_CallFunction",
                node_name="CreateWidget",
                position={"x": 300, "y": 100},
                input_pins=[
                    {"name": "OwningPlayer", "type": "object"},
                    {"name": "WidgetClass", "type": "class"}
                ],
                output_pins=[
                    {"name": "ReturnValue", "type": "object"},
                    {"name": "OutputExecPin", "type": "exec"}
                ],
                properties={"FunctionName": "CreateWidget"}
            ))
            node_id += 1

            # Add Add to Viewport node
            nodes.append(BlueprintNode(
                node_id=f"node_{node_id}",
                node_type="K2Node_CallFunction",
                node_name="AddToViewport",
                position={"x": 600, "y": 100},
                input_pins=[{"name": "Target", "type": "object"}],
                output_pins=[{"name": "OutputExecPin", "type": "exec"}],
                properties={"FunctionName": "AddToViewport"}
            ))
            node_id += 1

        return nodes

    def _generate_node_graph(self, blueprint_type: str) -> Dict[str, Any]:
        """
        Generate node graph structure.

        Args:
            blueprint_type: Type of blueprint

        Returns:
            Node graph dictionary
        """
        nodes = self._generate_nodes_for_system(blueprint_type)
        connections = self._generate_connections(nodes)

        return {
            "nodes": [self._node_to_dict(n) for n in nodes],
            "connections": connections,
            "type": blueprint_type
        }

    def _generate_event_nodes(self) -> List[BlueprintNode]:
        """
        Generate event nodes for graph.

        Returns:
            List of event nodes
        """
        return [
            BlueprintNode(
                node_id="event_begin_play",
                node_type="K2Node_Event",
                node_name="EventBeginPlay",
                position={"x": 0, "y": 0},
                input_pins=[],
                output_pins=[{"name": "OutputExecPin", "type": "exec"}],
                properties={"EventName": "ReceiveBeginPlay"}
            ),
            BlueprintNode(
                node_id="event_tick",
                node_type="K2Node_Event",
                node_name="EventTick",
                position={"x": 0, "y": 200},
                input_pins=[{"name": "DeltaTime", "type": "float"}],
                output_pins=[{"name": "OutputExecPin", "type": "exec"}],
                properties={"EventName": "ReceiveTick"}
            )
        ]

    def _generate_function_nodes(self, functions: List[str]) -> List[BlueprintNode]:
        """
        Generate function nodes for graph.

        Args:
            functions: List of function names

        Returns:
            List of function nodes
        """
        nodes = []
        y_offset = 400

        for func in functions:
            nodes.append(BlueprintNode(
                node_id=f"func_{func}",
                node_type="K2Node_CallFunction",
                node_name=func,
                position={"x": 300, "y": y_offset},
                input_pins=[{"name": "Self", "type": "object"}],
                output_pins=[{"name": "OutputExecPin", "type": "exec"}],
                properties={"FunctionName": func}
            ))
            y_offset += 150

        return nodes

    def _generate_connections(self, nodes: List[BlueprintNode]) -> List[Dict[str, str]]:
        """
        Generate node connections.

        Args:
            nodes: List of nodes

        Returns:
            List of connection dictionaries
        """
        connections = []

        if len(nodes) < 2:
            return connections

        # Connect nodes in sequence (exec pins)
        for i in range(len(nodes) - 1):
            current_node = nodes[i]
            next_node = nodes[i + 1]

            # Find exec output pin on current node
            exec_output = None
            for pin in current_node.output_pins:
                if pin.get("type") == "exec":
                    exec_output = pin["name"]
                    break

            # Find exec input pin on next node
            exec_input = None
            for pin in next_node.input_pins:
                if pin.get("type") == "exec":
                    exec_input = pin["name"]
                    break

            if exec_output and exec_input:
                connections.append({
                    "source_node": current_node.node_id,
                    "source_pin": f"{current_node.node_id}:{exec_output}",
                    "target_node": next_node.node_id,
                    "target_pin": f"{next_node.node_id}:{exec_input}"
                })

        return connections

    def _generate_variables(self, system: str) -> List[Dict[str, Any]]:
        """
        Generate variable definitions.

        Args:
            system: System name

        Returns:
            List of variable definitions
        """
        variables = []

        # Add common variables
        variables.append({
            "name": "Health",
            "type": "float",
            "default_value": "100.0",
            "instance_editable": True,
            "expose_on_spawn": True
        })

        variables.append({
            "name": "MaxHealth",
            "type": "float",
            "default_value": "100.0",
            "instance_editable": False,
            "expose_on_spawn": False
        })

        # Add system-specific variables
        if "Game" in system or "Gameplay" in system:
            variables.append({
                "name": "bIsAlive",
                "type": "boolean",
                "default_value": "true",
                "instance_editable": False,
                "expose_on_spawn": False
            })

        if "Widget" in system or "UI" in system:
            variables.append({
                "name": "StatusText",
                "type": "string",
                "default_value": '""',
                "instance_editable": True,
                "expose_on_spawn": False
            })

        return variables

    def _node_to_dict(self, node: BlueprintNode) -> Dict[str, Any]:
        """
        Convert BlueprintNode to dictionary.

        Args:
            node: Blueprint node

        Returns:
            Dictionary representation
        """
        return {
            "node_id": node.node_id,
            "node_type": node.node_type,
            "node_name": node.node_name,
            "position": node.position,
            "input_pins": node.input_pins,
            "output_pins": node.output_pins,
            "properties": node.properties
        }

    def validate_blueprint(self, graph: BlueprintGraph) -> List[str]:
        """
        Validate Blueprint graph structure.

        Args:
            graph: Blueprint graph to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check for at least one node
        if not graph.nodes:
            errors.append("Blueprint graph must have at least one node")

        # Check for unique node IDs
        node_ids = [n.node_id for n in graph.nodes]
        if len(node_ids) != len(set(node_ids)):
            errors.append("Blueprint graph has duplicate node IDs")

        # Check connections reference valid nodes
        valid_node_ids = set(node_ids)
        for conn in graph.connections:
            source_node = conn.get("source_node", "")
            target_node = conn.get("target_node", "")
            if source_node not in valid_node_ids:
                errors.append(f"Connection references invalid source node: {source_node}")
            if target_node not in valid_node_ids:
                errors.append(f"Connection references invalid target node: {target_node}")

        return errors
