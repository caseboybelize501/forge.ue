"""
Architect Agent Tests

Test brief → ProjectSpec generation.
"""
import pytest
from pathlib import Path
from ai.architect_agent import ArchitectAgent
from contracts.models.game_brief import GameBrief, Genre, Platform


class TestArchitectAgent:
    """Test architect agent functionality."""
    
    @pytest.fixture
    def architect(self, temp_dir):
        """Create architect agent instance."""
        templates_dir = temp_dir / "templates" / "interfaces"
        templates_dir.mkdir(parents=True)
        return ArchitectAgent(templates_dir)
    
    def test_design_architecture_returns_project_spec(self, architect, sample_game_brief):
        """Test that design_architecture returns valid ProjectSpec."""
        brief = GameBrief(**sample_game_brief)
        spec = architect.design_architecture(brief)
        
        assert spec is not None
        assert spec.project_id is not None
        assert spec.project_name is not None
    
    def test_action_rpg_includes_gas(self, architect):
        """Test FR-03: action/RPG brief includes GAS module."""
        brief = GameBrief(
            title="Action RPG Test",
            genre=Genre.RPG,
            platforms=[Platform.PC],
            mechanics=[],
            description="Test action RPG"
        )
        spec = architect.design_architecture(brief)
        
        # Should include GAS subsystem
        assert any("GAS" in str(s) for s in spec.subsystems)
    
    def test_multiplayer_includes_replication(self, architect):
        """Test FR-03: multiplayer brief includes replication."""
        brief = GameBrief(
            title="Multiplayer Test",
            genre=Genre.MULTIPLAYER,
            platforms=[Platform.PC],
            mechanics=[],
            description="Test multiplayer"
        )
        spec = architect.design_architecture(brief)
        
        # Should include replication subsystem
        assert any("REPLICATION" in str(s) for s in spec.subsystems)
    
    def test_ubt_deps_cycle_free(self, architect, sample_game_brief):
        """Test FR-22: UBT module deps are cycle-free."""
        brief = GameBrief(**sample_game_brief)
        spec = architect.design_architecture(brief)
        
        # Verify no cycles in module graph
        assert self._is_dag(spec.ubt_module_deps)
    
    def _is_dag(self, graph):
        """Check if graph is a DAG (no cycles)."""
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if node not in visited:
                if has_cycle(node):
                    return False
        return True
