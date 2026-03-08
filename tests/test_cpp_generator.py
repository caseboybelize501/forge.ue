"""
CPP Generator Tests

Test ModuleSpec → valid C++ headers.
"""
import pytest
from pathlib import Path
from engine.cpp_generator import CppGenerator
from contracts.models.project_spec import ModuleSpec, ModuleType


class TestCppGenerator:
    """Test C++ generator functionality."""
    
    @pytest.fixture
    def generator(self):
        """Create C++ generator instance."""
        return CppGenerator()
    
    def test_generate_header_contains_uclass(self, generator):
        """Test NFR-03: Generated headers contain UCLASS macro."""
        module = ModuleSpec(
            module_name="TestModule",
            module_type=ModuleType.CORE,
            dependencies=[],
        )
        header = generator._generate_header(module, "TestCharacter")
        
        assert "UCLASS" in header.content
        assert "GENERATED_BODY" in header.content
    
    def test_generate_header_contains_uproperty(self, generator):
        """Test NFR-03: Properties have UPROPERTY macro."""
        pass
    
    def test_generate_header_contains_ufunction(self, generator):
        """Test NFR-03: Functions have UFUNCTION macro."""
        pass
    
    def test_generate_cpp_implements_header(self, generator):
        """Test Pass 2: .cpp implements paired .h exactly."""
        pass
    
    def test_generated_code_follows_ue5_standards(self, generator):
        """Test NFR-03: Generated code follows UE5 coding standards."""
        pass
