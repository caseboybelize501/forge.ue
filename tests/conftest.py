"""
Pytest Fixtures and Configuration

Shared fixtures for FORGE test suite.
"""
import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """
    Create temporary directory for test output.
    
    Yields:
        Path to temporary directory
    """
    tmp = tempfile.mkdtemp()
    yield Path(tmp)
    shutil.rmtree(tmp)


@pytest.fixture
def sample_game_brief():
    """
    Sample game brief for testing.
    
    Returns:
        Sample GameBrief dictionary
    """
    return {
        "title": "Test Game",
        "genre": "action",
        "platforms": ["pc"],
        "mechanics": [
            {"name": "Combat", "description": "Basic combat", "priority": 3}
        ],
        "description": "A test game for testing"
    }


@pytest.fixture
def sample_project_spec():
    """
    Sample project specification for testing.
    
    Returns:
        Sample ProjectSpec dictionary
    """
    return {
        "project_id": "test-001",
        "project_name": "TestGame",
        "modules": [],
        "subsystems": [],
        "cpp_files": [],
        "blueprint_files": [],
        "ubt_module_deps": {},
        "platform_targets": ["Win64"],
        "estimated_compile_min": 5
    }


@pytest.fixture
def mock_ue5_root(temp_dir):
    """
    Mock UE5 installation directory.
    
    Args:
        temp_dir: Temporary directory fixture
        
    Yields:
        Path to mock UE5 root
    """
    ue5_root = temp_dir / "UE_5.3"
    ue5_root.mkdir()
    (ue5_root / "Engine").mkdir()
    (ue5_root / "Engine" / "Binaries").mkdir(parents=True)
    yield ue5_root
