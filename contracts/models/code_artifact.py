"""
Code Artifact Schema — Level 0 Foundation

Defines schemas for generated code artifacts.

Dependencies: None (foundation file)
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator


class CppFile(BaseModel):
    """
    Generated C++ implementation file.
    
    Attributes:
        path: File path relative to project root
        content: File content
        module: UE5 module name
        dependencies: List of file dependencies
    """
    path: str
    content: str
    module: str
    dependencies: List[str] = Field(default_factory=list)
    
    @field_validator('path')
    @classmethod
    def path_not_empty(cls, v: str) -> str:
        """Validate path is not empty."""
        if not v or not v.strip():
            raise ValueError('path cannot be empty')
        return v.strip()
    
    @field_validator('content')
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        """Validate content is not empty."""
        if not v or not v.strip():
            raise ValueError('content cannot be empty')
        return v.strip()
    
    @field_validator('module')
    @classmethod
    def module_not_empty(cls, v: str) -> str:
        """Validate module is not empty."""
        if not v or not v.strip():
            raise ValueError('module cannot be empty')
        return v.strip()


class HeaderFile(BaseModel):
    """
    Generated C++ header file.
    
    Attributes:
        path: File path relative to project root
        content: File content
        module: UE5 module name
        is_interface: Whether this is an interface header
        uclass_name: UCLASS name if applicable
    """
    path: str
    content: str
    module: str
    is_interface: bool = False
    uclass_name: Optional[str] = None
    
    @field_validator('path')
    @classmethod
    def path_not_empty(cls, v: str) -> str:
        """Validate path is not empty."""
        if not v or not v.strip():
            raise ValueError('path cannot be empty')
        return v.strip()
    
    @field_validator('content')
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        """Validate content is not empty."""
        if not v or not v.strip():
            raise ValueError('content cannot be empty')
        return v.strip()
    
    @field_validator('module')
    @classmethod
    def module_not_empty(cls, v: str) -> str:
        """Validate module is not empty."""
        if not v or not v.strip():
            raise ValueError('module cannot be empty')
        return v.strip()


class BlueprintNode(BaseModel):
    """
    Blueprint graph node.
    
    Attributes:
        node_id: Unique node identifier
        node_type: Type of node (function, event, variable, etc.)
        position: X,Y position in graph editor
        inputs: Input pin connections
        outputs: Output pin connections
        properties: Node-specific properties
    """
    node_id: str
    node_type: str
    position: Dict[str, int]
    inputs: Dict[str, str] = Field(default_factory=dict)
    outputs: Dict[str, str] = Field(default_factory=dict)
    properties: Dict[str, Any] = Field(default_factory=dict)
    
    @field_validator('node_id')
    @classmethod
    def node_id_not_empty(cls, v: str) -> str:
        """Validate node_id is not empty."""
        if not v or not v.strip():
            raise ValueError('node_id cannot be empty')
        return v.strip()
    
    @field_validator('node_type')
    @classmethod
    def node_type_not_empty(cls, v: str) -> str:
        """Validate node_type is not empty."""
        if not v or not v.strip():
            raise ValueError('node_type cannot be empty')
        return v.strip()


class BlueprintGraph(BaseModel):
    """
    Generated Blueprint graph as structured JSON.
    
    Attributes:
        path: File path relative to Content/
        graph_name: Name of the Blueprint graph
        nodes: List of nodes in the graph
        connections: List of node connections
    """
    path: str
    graph_name: str
    nodes: List[BlueprintNode]
    connections: List[Dict[str, str]]
    
    @field_validator('path')
    @classmethod
    def path_not_empty(cls, v: str) -> str:
        """Validate path is not empty."""
        if not v or not v.strip():
            raise ValueError('path cannot be empty')
        return v.strip()
    
    @field_validator('graph_name')
    @classmethod
    def graph_name_not_empty(cls, v: str) -> str:
        """Validate graph_name is not empty."""
        if not v or not v.strip():
            raise ValueError('graph_name cannot be empty')
        return v.strip()
    
    @field_validator('nodes')
    @classmethod
    def at_least_one_node(cls, v: List[BlueprintNode]) -> List[BlueprintNode]:
        """Validate at least one node exists."""
        if not v or len(v) == 0:
            raise ValueError('at least one node is required')
        return v
