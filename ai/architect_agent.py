"""
Architect Agent — Level 1 Core Agent

Transforms GameBrief → ProjectSpec + UBT Module Graph.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- templates/interfaces/*.h (L0-009 to L0-018)
"""
from typing import List, Dict, Optional
from pathlib import Path

from contracts.models.game_brief import GameBrief, Genre, Platform
from contracts.models.project_spec import ProjectSpec, ModuleSpec, SubsystemRef
from contracts.models.code_artifact import HeaderFile


class ArchitectAgent:
    """
    Architect Agent for FORGE pipeline.
    
    Reads game brief and designs complete UE5 project architecture:
    - Selects appropriate subsystems based on genre
    - Designs module graph for UBT
    - Allocates systems to C++ vs Blueprint
    - Emits ProjectSpec for human review (GATE-1)
    
    Attributes:
        templates_dir: Path to interface header templates
        interface_headers: Loaded interface headers
    """
    
    def __init__(self, templates_dir: Path):
        """
        Initialize architect agent.
        
        Args:
            templates_dir: Path to templates/interfaces/ directory
        """
        self.templates_dir = templates_dir
        self.interface_headers: Dict[str, HeaderFile] = {}
    
    def design_architecture(self, brief: GameBrief) -> ProjectSpec:
        """
        Generate full project architecture from game brief.
        
        Args:
            brief: Parsed game brief
            
        Returns:
            Complete ProjectSpec with modules, subsystems, and file lists
        """
        pass
    
    def _select_subsystems(self, genre: Genre) -> List[SubsystemRef]:
        """
        Select UE5 subsystems based on genre.
        
        Args:
            genre: Game genre
            
        Returns:
            List of required subsystems
        """
        pass
    
    def _design_module_graph(self, brief: GameBrief) -> Dict[str, List[str]]:
        """
        Design UBT module dependency graph.
        
        Args:
            brief: Game brief
            
        Returns:
            Module dependency graph (must be cycle-free)
        """
        pass
    
    def _allocate_languages(self, brief: GameBrief) -> Dict[str, str]:
        """
        Allocate systems to C++ or Blueprint.
        
        Args:
            brief: Game brief
            
        Returns:
            Mapping of system → language allocation
        """
        pass
    
    def _load_interface_headers(self) -> Dict[str, HeaderFile]:
        """
        Load immutable interface headers from templates/.
        
        Returns:
            Dictionary of header name → HeaderFile content
        """
        pass
