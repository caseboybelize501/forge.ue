"""
Code Artifact Schema — Level 0 Foundation

Defines schemas for generated code artifacts.
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class CppFile(BaseModel):
    """Generated C++ implementation file."""
    path: str
    content: str
    module: str
    dependencies: List[str] = []


class HeaderFile(BaseModel):
    """Generated C++ header file."""
    path: str
    content: str
    module: str
    is_interface: bool = False
    uclass_name: Optional[str] = None


class BlueprintNode(BaseModel):
    """Blueprint graph node."""
    node_id: str
    node_type: str
    position: Dict[str, int]
    inputs: Dict[str, str] = {}
    outputs: Dict[str, str] = {}
    properties: Dict[str, Any] = {}


class BlueprintGraph(BaseModel):
    """Generated Blueprint graph as structured JSON."""
    path: str
    graph_name: str
    nodes: List[BlueprintNode]
    connections: List[Dict[str, str]]
