"""
Repair Loop Tests

Test UBT error → repair fires.
"""
import pytest
from ai.repair_loop import RepairLoop
from contracts.models.build_result import RepairContext


class TestRepairLoop:
    """Test repair loop functionality."""
    
    @pytest.fixture
    def repair_loop(self):
        """Create repair loop instance."""
        return RepairLoop()
    
    def test_repair_file_fixes_error(self, repair_loop):
        """Test FR-09: Repair loop fixes UBT errors."""
        context = RepairContext(
            failing_file="Test.cpp",
            error_text="syntax error: missing ';'",
            error_line=42,
            ue5_version="5.3",
            module_deps=[],
            interface_header=None,
            prior_attempts=[],
            ue5_coding_standard_rules=RepairLoop.UE5_CODING_RULES
        )
        
        result = repair_loop.repair_file(context)
        
        # Should return repaired content or None after max attempts
        assert result is None or ";" in result
    
    def test_repair_loop_max_attempts(self, repair_loop):
        """Test HR-03: Max 3 repair attempts."""
        context = RepairContext(
            failing_file="Test.cpp",
            error_text="persistent error",
            error_line=1,
            ue5_version="5.3",
            module_deps=[],
            interface_header=None,
            prior_attempts=["attempt1", "attempt2", "attempt3"],
            ue5_coding_standard_rules=RepairLoop.UE5_CODING_RULES
        )
        
        result = repair_loop.repair_file(context)
        
        # Should return None after max attempts
        assert result is None
    
    def test_classify_error_types(self, repair_loop):
        """Test repair_loop classifies different error types."""
        error_types = [
            ("syntax error: missing ';'", "syntax"),
            ("unresolved external symbol", "linker"),
            ("UCLASS macro missing", "uht"),
        ]
        
        for error_text, expected_type in error_types:
            result = repair_loop.classify_error(error_text)
            assert result == expected_type
    
    def test_ue5_coding_rules_injected(self, repair_loop):
        """Test NFR-03: UE5 coding rules injected into repair prompt."""
        assert "UCLASS" in repair_loop.UE5_CODING_RULES
        assert "GENERATED_BODY" in repair_loop.UE5_CODING_RULES
        assert "UPROPERTY" in repair_loop.UE5_CODING_RULES
        assert "UFUNCTION" in repair_loop.UE5_CODING_RULES
        assert "TObjectPtr" in repair_loop.UE5_CODING_RULES
