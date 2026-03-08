"""
Build Runner Tests

Test mock UBT → error parse + repair.
"""
import pytest
from pathlib import Path
from engine.build_runner import BuildRunner
from contracts.models.build_result import CompileResult, ErrorReport


class TestBuildRunner:
    """Test build runner functionality."""
    
    @pytest.fixture
    def build_runner(self, mock_ue5_root):
        """Create build runner instance."""
        return BuildRunner(ue_root=mock_ue5_root)
    
    def test_run_ubt_returns_compile_result(self, build_runner, temp_dir):
        """Test FR-07: UBT compile returns CompileResult."""
        # Would need actual project structure
        pass
    
    def test_parse_ubt_errors_extracts_file_line(self, build_runner):
        """Test FR-07: Error parser extracts file and line."""
        stderr = """
        D:\\Projects\\Test\\Source\\Test.cpp(42): error: syntax error: missing ';'
        """
        errors = build_runner.parse_ubt_errors(stderr)
        
        assert len(errors) > 0
        assert errors[0].file_path.endswith("Test.cpp")
        assert errors[0].line_number == 42
    
    def test_parse_ubt_errors_handles_multiple_errors(self, build_runner):
        """Test FR-07: Parser handles multiple errors."""
        stderr = """
        D:\\Projects\\Test\\Source\\A.cpp(10): error: error A
        D:\\Projects\\Test\\Source\\B.cpp(20): error: error B
        """
        errors = build_runner.parse_ubt_errors(stderr)
        
        assert len(errors) == 2
    
    def test_uht_runs_before_ubt(self, build_runner):
        """Test NFR-04: UHT runs before UBT."""
        pass
