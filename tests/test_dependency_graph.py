"""
Dependency Graph Tests

Test Graph A + Graph B cycle detection.
"""
import pytest
from typing import Dict, List, Tuple


class TestDependencyGraph:
    """Test dependency graph validation."""
    
    # Graph A from dependency_graph.md
    GRAPH_A = {
        'C0': [],
        'C1': [],
        'AI0': ['C0', 'C1'],
        'AI1': ['C0'],
        'E0': ['C0'],
        'E1': ['C0', 'C1', 'AI0'],
        'E2': ['C0', 'C1', 'E1'],
        'E3': ['C0', 'C1', 'E2'],
        'E4': ['C0', 'C1', 'E2'],
        'E5': ['C0', 'E3', 'AI1'],
        'E6': ['C0', 'E5'],
        'E7': ['C0', 'E6'],
        'S0': ['C0', 'C1', 'E1', 'E2'],
        'S1': ['C0', 'C1', 'AI0'],
        'S10': ['S0', 'S1'],
    }
    
    def test_graph_a_no_cycles(self):
        """Test Graph A is cycle-free."""
        has_cycle, cycles = self.detect_cycles(self.GRAPH_A)
        assert not has_cycle, f"Cycles detected in Graph A: {cycles}"
    
    def test_graph_b_no_cycles(self):
        """Test Graph B (UBT modules) is cycle-free."""
        graph_b = {
            'MyGameCore': [],
            'MyGameGameFramework': ['MyGameCore'],
            'MyGameCombatSystem': ['MyGameCore', 'MyGameGameFramework'],
            'MyGameUI': ['MyGameCore', 'MyGameGameFramework', 'MyGameCombatSystem'],
            'MyGamePlatform': ['MyGameCore', 'MyGameGameFramework', 'MyGameCombatSystem', 'MyGameUI'],
        }
        
        has_cycle, cycles = self.detect_cycles(graph_b)
        assert not has_cycle, f"Cycles detected in Graph B: {cycles}"
    
    def test_topological_levels_valid(self):
        """Test topological level assignment is valid."""
        levels = self.assign_levels(self.GRAPH_A)
        
        # Verify level constraints
        for node, level in levels.items():
            for dep in self.GRAPH_A.get(node, []):
                assert levels[dep] < level, \
                    f"Node {node} (L{level}) depends on {dep} (L{levels[dep]})"
    
    def test_all_nodes_reachable(self):
        """Test all nodes are reachable from L0."""
        # All nodes should have a path from L0 nodes
        l0_nodes = [n for n, deps in self.GRAPH_A.items() if not deps]
        reachable = self.find_reachable(self.GRAPH_A, l0_nodes)
        
        assert len(reachable) == len(self.GRAPH_A), \
            f"Unreachable nodes: {set(self.GRAPH_A.keys()) - reachable}"
    
    def detect_cycles(self, graph: Dict[str, List[str]]) -> Tuple[bool, List[List[str]]]:
        """DFS-based cycle detection."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {node: WHITE for node in graph}
        cycles = []
        
        def dfs(node: str, path: List[str]) -> bool:
            color[node] = GRAY
            for neighbor in graph.get(node, []):
                if neighbor not in color:
                    continue
                if color[neighbor] == GRAY:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
                    return True
                if color[neighbor] == WHITE and dfs(neighbor, path + [neighbor]):
                    return True
            color[node] = BLACK
            return False
        
        for node in graph:
            if color[node] == WHITE:
                dfs(node, [node])
        
        return (len(cycles) > 0, cycles)
    
    def assign_levels(self, graph: Dict[str, List[str]]) -> Dict[str, int]:
        """Assign topological levels."""
        levels = {}
        
        def get_level(node: str, visited: set) -> int:
            if node in levels:
                return levels[node]
            if node in visited:
                raise ValueError(f"Cycle at {node}")
            visited.add(node)
            
            deps = graph.get(node, [])
            if not deps:
                levels[node] = 0
            else:
                max_dep = max(get_level(d, visited) for d in deps if d in graph)
                levels[node] = max_dep + 1
            
            visited.remove(node)
            return levels[node]
        
        for node in graph:
            get_level(node, set())
        
        return levels
    
    def find_reachable(self, graph: Dict[str, List[str]], start_nodes: List[str]) -> set:
        """Find all reachable nodes from start nodes."""
        # Build reverse graph
        reverse = {n: [] for n in graph}
        for node, deps in graph.items():
            for dep in deps:
                if dep in reverse:
                    reverse[dep].append(node)
        
        reachable = set()
        queue = list(start_nodes)
        
        while queue:
            node = queue.pop(0)
            if node in reachable:
                continue
            reachable.add(node)
            queue.extend(reverse.get(node, []))
        
        return reachable
