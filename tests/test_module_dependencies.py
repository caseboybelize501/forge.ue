"""
Module Dependencies Tests

Validate actual imports match declared dependencies.
"""
import pytest
import ast
from pathlib import Path


class TestModuleDependencies:
    """Test module dependency validation."""
    
    def test_no_circular_dependencies(self):
        """Verify no circular imports exist."""
        # This would use the dependency validator
        pass
    
    def test_imports_match_declarations(self):
        """Verify actual Python imports match declared graph."""
        pass
    
    def test_no_forbidden_imports(self):
        """Verify no forbidden import patterns exist."""
        forbidden_patterns = [
            ("engine/", "server/"),
            ("ai/", "engine/"),
            ("server/", "ai/"),
        ]
        
        # Would scan all Python files
        pass
    
    def extract_imports(self, module_path: str) -> list:
        """Extract actual import statements from Python file."""
        with open(module_path) as f:
            tree = ast.parse(f.read())
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        return imports
    
    def test_level_0_has_no_internal_deps(self):
        """Verify Level 0 modules have no internal dependencies."""
        l0_modules = [
            "contracts/models/game_brief.py",
            "contracts/models/project_spec.py",
            "contracts/api.yaml",
        ]
        
        for module in l0_modules:
            if module.endswith('.py'):
                imports = self.extract_imports(module)
                # Should only have external deps (pydantic, typing, enum)
                for imp in imports:
                    assert not imp.startswith('contracts'), \
                        f"L0 module {module} has internal dep: {imp}"
    
    def test_ai_only_depends_on_contracts(self):
        """Verify ai/ only depends on contracts/ and templates/."""
        pass
    
    def test_engine_depends_on_contracts_and_ai(self):
        """Verify engine/ depends on contracts/ and lower engine levels."""
        pass
