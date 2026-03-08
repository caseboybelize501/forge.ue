"""
Build Result Schema — Level 0 Foundation

Defines schemas for build, test, and packaging results.
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class ErrorReport(BaseModel):
    """Structured error report from UBT/UHT."""
    file_path: str
    line_number: Optional[int]
    error_type: str
    error_message: str
    suggestion: Optional[str] = None


class RepairContext(BaseModel):
    """Context for repair_loop operations."""
    failing_file: str
    error_text: str
    error_line: Optional[int]
    ue5_version: str
    module_deps: List[str]
    interface_header: Optional[str]
    prior_attempts: List[str]
    ue5_coding_standard_rules: str


class CompileResult(BaseModel):
    """Result of UBT/UHT compilation."""
    success: bool
    errors: List[ErrorReport]
    warnings: List[str]
    duration_seconds: float
    timestamp: datetime


class TestSpec(BaseModel):
    """Test specification for a system."""
    test_name: str
    test_type: Literal["automation", "blueprint", "platform_guard"]
    target_system: str
    assertions: List[Dict[str, Any]]
    expected_result: str


class TestResult(BaseModel):
    """Result of test execution."""
    success: bool
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    details: List[Dict[str, Any]]
    duration_seconds: float
    timestamp: datetime


class PackageResult(BaseModel):
    """Result of platform packaging."""
    success: bool
    platform: str
    output_path: str
    size_bytes: int
    duration_seconds: float
    timestamp: datetime
