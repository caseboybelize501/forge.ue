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

from contracts.models.game_brief import GameBrief, Genre, Platform, MechanicSpec
from contracts.models.project_spec import (
    ProjectSpec,
    ModuleSpec,
    ModuleType,
    SubsystemRef,
    Pattern,
)
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

    # Genre to subsystem mapping
    GENRE_SUBSYSTEM_MAP = {
        Genre.ACTION: [
            SubsystemRef.GAS,
            SubsystemRef.ENHANCED_INPUT,
            SubsystemRef.REPLICATION,
        ],
        Genre.RPG: [
            SubsystemRef.GAS,
            SubsystemRef.ENHANCED_INPUT,
            SubsystemRef.WORLD_PARTITION,
            SubsystemRef.LEVEL_STREAMING,
        ],
        Genre.OPEN_WORLD: [
            SubsystemRef.WORLD_PARTITION,
            SubsystemRef.LEVEL_STREAMING,
            SubsystemRef.ONLINE_SUBSYSTEM,
            SubsystemRef.AGGRESSIVE_LOD,
        ],
        Genre.MULTIPLAYER: [
            SubsystemRef.GAS,
            SubsystemRef.REPLICATION,
            SubsystemRef.ONLINE_SUBSYSTEM,
        ],
        Genre.MOBILE: [
            SubsystemRef.ENHANCED_INPUT,
            SubsystemRef.REDUCED_TICK,
            SubsystemRef.CUSTOM_STATE_MACHINE,
        ],
        Genre.PUZZLE: [
            SubsystemRef.ENHANCED_INPUT,
            SubsystemRef.CUSTOM_STATE_MACHINE,
        ],
        Genre.STRATEGY: [
            SubsystemRef.WORLD_PARTITION,
            SubsystemRef.LEVEL_STREAMING,
            SubsystemRef.CUSTOM_STATE_MACHINE,
        ],
    }

    # Genre to module type mapping
    GENRE_MODULE_MAP = {
        Genre.ACTION: ModuleType.GAME_FRAMEWORK,
        Genre.RPG: ModuleType.GENRE_SYSTEM,
        Genre.OPEN_WORLD: ModuleType.GENRE_SYSTEM,
        Genre.MULTIPLAYER: ModuleType.GAME_FRAMEWORK,
        Genre.MOBILE: ModuleType.CORE,
        Genre.PUZZLE: ModuleType.CORE,
        Genre.STRATEGY: ModuleType.GENRE_SYSTEM,
    }

    def __init__(self, templates_dir: Path):
        """
        Initialize architect agent.

        Args:
            templates_dir: Path to templates/interfaces/ directory
        """
        self.templates_dir = templates_dir
        self.interface_headers: Dict[str, HeaderFile] = {}
        self._load_interface_headers()

    def design_architecture(self, brief: GameBrief) -> ProjectSpec:
        """
        Generate full project architecture from game brief.

        Args:
            brief: Parsed game brief

        Returns:
            Complete ProjectSpec with modules, subsystems, and file lists
        """
        # Select subsystems based on genre
        subsystems = self._select_subsystems(brief.genre)
        
        # Design module dependency graph
        module_graph = self._design_module_graph(brief)
        
        # Allocate languages (C++ vs Blueprint)
        language_allocation = self._allocate_languages(brief)
        
        # Create module specs
        modules = self._create_module_specs(brief, module_graph)
        
        # Generate project spec
        project_spec = ProjectSpec(
            project_id=f"PROJ_{brief.title.upper().replace(' ', '_')}",
            project_name=brief.title,
            modules=modules,
            subsystems=subsystems,
            cpp_files=self._generate_cpp_file_list(modules),
            blueprint_files=self._generate_blueprint_file_list(modules),
            ubt_module_deps=module_graph,
            platform_targets=[p.value for p in brief.platforms],
            estimated_compile_min=self._estimate_compile_time(modules),
            genre_patterns=self._get_genre_patterns(brief.genre),
        )
        
        return project_spec

    def _select_subsystems(self, genre: Genre) -> List[SubsystemRef]:
        """
        Select UE5 subsystems based on genre.

        Args:
            genre: Game genre

        Returns:
            List of required subsystems
        """
        return self.GENRE_SUBSYSTEM_MAP.get(genre, [SubsystemRef.ENHANCED_INPUT])

    def _design_module_graph(self, brief: GameBrief) -> Dict[str, List[str]]:
        """
        Design UBT module dependency graph.

        Args:
            brief: Game brief

        Returns:
            Module dependency graph (must be cycle-free)
        """
        # Core module depends on nothing
        # GameFramework depends on Core
        # GenreSystem depends on GameFramework
        # UI depends on GameFramework
        # Platform depends on Core
        
        module_type = self.GENRE_MODULE_MAP.get(brief.genre, ModuleType.CORE)
        
        graph = {
            f"{brief.title}Core": [],
            f"{brief.title}GameFramework": [f"{brief.title}Core"],
        }
        
        if module_type == ModuleType.GENRE_SYSTEM:
            graph[f"{brief.title}GenreSystem"] = [f"{brief.title}GameFramework"]
        
        graph[f"{brief.title}UI"] = [f"{brief.title}GameFramework"]
        graph[f"{brief.title}Platform"] = [f"{brief.title}Core"]
        
        return graph

    def _allocate_languages(self, brief: GameBrief) -> Dict[str, str]:
        """
        Allocate systems to C++ or Blueprint.

        Args:
            brief: Game brief

        Returns:
            Mapping of system → language allocation
        """
        allocation = {}
        
        # Core systems in C++
        allocation["Core"] = "cpp"
        allocation["GameFramework"] = "cpp"
        
        # Genre-specific systems based on complexity
        if brief.genre in [Genre.RPG, Genre.OPEN_WORLD, Genre.STRATEGY]:
            allocation["GenreSystem"] = "cpp"
        else:
            allocation["GenreSystem"] = "blueprint"
        
        # UI typically in Blueprint
        allocation["UI"] = "blueprint"
        
        # Platform layer in C++
        allocation["Platform"] = "cpp"
        
        return allocation

    def _create_module_specs(self, brief: GameBrief, module_graph: Dict[str, List[str]]) -> List[ModuleSpec]:
        """
        Create module specifications from module graph.

        Args:
            brief: Game brief
            module_graph: Module dependency graph

        Returns:
            List of module specifications
        """
        modules = []
        
        for module_name, dependencies in module_graph.items():
            # Determine module type
            if "Core" in module_name and module_name != "Core":
                module_type = ModuleType.CORE
            elif "GameFramework" in module_name:
                module_type = ModuleType.GAME_FRAMEWORK
            elif "GenreSystem" in module_name:
                module_type = ModuleType.GENRE_SYSTEM
            elif "UI" in module_name:
                module_type = ModuleType.UI
            elif "Platform" in module_name:
                module_type = ModuleType.PLATFORM
            else:
                module_type = ModuleType.CORE
            
            module_spec = ModuleSpec(
                module_name=module_name,
                module_type=module_type,
                dependencies=dependencies,
                dependency_modules=["Engine", "CoreUObject"],
                platform_guards=[p.value.upper() for p in brief.platforms if p != Platform.PC],
            )
            modules.append(module_spec)
        
        return modules

    def _generate_cpp_file_list(self, modules: List[ModuleSpec]) -> List[str]:
        """
        Generate list of C++ files to create.

        Args:
            modules: List of module specs

        Returns:
            List of C++ file paths
        """
        files = []
        for module in modules:
            module_base = module.module_name.replace(" ", "")
            files.append(f"Source/{module_base}/{module_base}.h")
            files.append(f"Source/{module_base}/{module_base}.cpp")
        return files

    def _generate_blueprint_file_list(self, modules: List[ModuleSpec]) -> List[str]:
        """
        Generate list of Blueprint files to create.

        Args:
            modules: List of module specs

        Returns:
            List of Blueprint file paths
        """
        files = []
        for module in modules:
            module_base = module.module_name.replace(" ", "")
            files.append(f"Content/Blueprints/{module_base}_BP.uasset")
        return files

    def _estimate_compile_time(self, modules: List[ModuleSpec]) -> int:
        """
        Estimate compile time in minutes.

        Args:
            modules: List of module specs

        Returns:
            Estimated compile time
        """
        # Base time + 2 minutes per module
        return 5 + (len(modules) * 2)

    def _get_genre_patterns(self, genre: Genre) -> List[str]:
        """
        Get genre-specific patterns.

        Args:
            genre: Game genre

        Returns:
            List of pattern IDs
        """
        patterns = {
            Genre.ACTION: ["action_combat", "action_movement"],
            Genre.RPG: ["rpg_inventory", "rpg_dialogue", "rpg_stats"],
            Genre.OPEN_WORLD: ["openworld_streaming", "openworld_lod"],
            Genre.MULTIPLAYER: ["multiplayer_replication", "multiplayer_session"],
            Genre.MOBILE: ["mobile_input", "mobile_performance"],
            Genre.PUZZLE: ["puzzle_interaction", "puzzle_state"],
            Genre.STRATEGY: ["strategy_ai", "strategy_pathfinding"],
        }
        return patterns.get(genre, [])

    def _load_interface_headers(self) -> Dict[str, HeaderFile]:
        """
        Load immutable interface headers from templates/.

        Returns:
            Dictionary of header name → HeaderFile content
        """
        interfaces_dir = self.templates_dir / "interfaces"
        
        if not interfaces_dir.exists():
            return self.interface_headers
        
        # Load all interface headers
        interface_files = list(interfaces_dir.glob("*.h"))
        
        for header_path in interface_files:
            try:
                with open(header_path, 'r') as f:
                    content = f.read()
                    header_file = HeaderFile(
                        path=str(header_path),
                        content=content,
                        module="Interfaces",
                        is_interface=True,
                    )
                    self.interface_headers[header_path.stem] = header_file
            except (IOError, OSError):
                continue
        
        return self.interface_headers
