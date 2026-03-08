"""
Build Result Schema — Level 0 Foundation

Defines schemas for build, test, and packaging results.

Dependencies:
- contracts.models.code_artifact (for ErrorReport forward reference)
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class ErrorReport(BaseModel):
    """
    Structured error report from UBT/UHT.
    
    Attributes:
        file_path: Path to file with error
        line_number: Line number of error (if available)
        error_type: Type of error (syntax, linker, etc.)
        error_message: Full error message
        suggestion: Optional fix suggestion
    """
    file_path: str
    line_number: Optional[int] = None
    error_type: str
    error_message: str
    suggestion: Optional[str] = None
    
    @field_validator('file_path')
    @classmethod
    def file_path_not_empty(cls, v: str) -> str:
        """Validate file_path is not empty."""
        if not v or not v.strip():
            raise ValueError('file_path cannot be empty')
        return v.strip()
    
    @field_validator('error_type')
    @classmethod
    def error_type_not_empty(cls, v: str) -> str:
        """Validate error_type is not empty."""
        if not v or not v.strip():
            raise ValueError('error_type cannot be empty')
        return v.strip()
    
    @field_validator('error_message')
    @classmethod
    def error_message_not_empty(cls, v: str) -> str:
        """Validate error_message is not empty."""
        if not v or not v.strip():
            raise ValueError('error_message cannot be empty')
        return v.strip()


class RepairContext(BaseModel):
    """
    Context for repair_loop operations.
    
    Attributes:
        failing_file: Path to file being repaired
        error_text: Full error text from UBT/UHT
        error_line: Line number of error
        ue5_version: UE5 version string
        module_deps: List of module dependencies
        interface_header: Related interface header (if any)
        prior_attempts: List of prior repair attempts
        ue5_coding_standard_rules: UE5 coding rules for repair
    """
    failing_file: str
    error_text: str
    error_line: Optional[int] = None
    ue5_version: str
    module_deps: List[str]
    interface_header: Optional[str] = None
    prior_attempts: List[str] = Field(default_factory=list)
    ue5_coding_standard_rules: str
    
    @field_validator('failing_file')
    @classmethod
    def failing_file_not_empty(cls, v: str) -> str:
        """Validate failing_file is not empty."""
        if not v or not v.strip():
            raise ValueError('failing_file cannot be empty')
        return v.strip()
    
    @field_validator('error_text')
    @classmethod
    def error_text_not_empty(cls, v: str) -> str:
        """Validate error_text is not empty."""
        if not v or not v.strip():
            raise ValueError('error_text cannot be empty')
        return v.strip()
    
    @field_validator('ue5_version')
    @classmethod
    def ue5_version_not_empty(cls, v: str) -> str:
        """Validate ue5_version is not empty."""
        if not v or not v.strip():
            raise ValueError('ue5_version cannot be empty')
        return v.strip()
    
    @field_validator('ue5_coding_standard_rules')
    @classmethod
    def coding_rules_not_empty(cls, v: str) -> str:
        """Validate ue5_coding_standard_rules is not empty."""
        if not v or not v.strip():
            raise ValueError('ue5_coding_standard_rules cannot be empty')
        return v.strip()


class CompileResult(BaseModel):
    """
    Result of UBT/UHT compilation.
    
    Attributes:
        success: Whether compilation succeeded
        errors: List of error reports
        warnings: List of warning messages
        duration_seconds: Compilation duration
        timestamp: Compilation timestamp
    """
    success: bool
    errors: List[ErrorReport] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    duration_seconds: float
    timestamp: datetime
    
    @field_validator('duration_seconds')
    @classmethod
    def duration_positive(cls, v: float) -> float:
        """Validate duration is non-negative."""
        if v < 0:
            raise ValueError('duration_seconds must be non-negative')
        return v


class TestSpec(BaseModel):
    """
    Test specification for a system.

    Attributes:
        test_name: Name of the test
        test_type: Type of test (automation, blueprint, platform_guard)
        target_system: System being tested
        assertions: List of test assertions
        expected_result: Expected test result
    """
    test_name: str
    test_type: Literal["automation", "blueprint", "platform_guard"]
    target_system: str
    assertions: List[Dict[str, Any]] = Field(default_factory=list)
    expected_result: str

    @field_validator('test_name')
    @classmethod
    def test_name_not_empty(cls, v: str) -> str:
        """Validate test_name is not empty."""
        if not v or not v.strip():
            raise ValueError('test_name cannot be empty')
        return v.strip()

    @field_validator('target_system')
    @classmethod
    def target_system_not_empty(cls, v: str) -> str:
        """Validate target_system is not empty."""
        if not v or not v.strip():
            raise ValueError('target_system cannot be empty')
        return v.strip()

    @field_validator('expected_result')
    @classmethod
    def expected_result_not_empty(cls, v: str) -> str:
        """Validate expected_result is not empty."""
        if not v or not v.strip():
            raise ValueError('expected_result cannot be empty')
        return v.strip()


class AssertionSpec(BaseModel):
    """
    Individual test assertion specification.

    Attributes:
        name: Assertion name
        condition: Condition to test (as string expression)
        expected_value: Expected value for the condition
        actual_value: Actual value (populated during test execution)
        message: Optional assertion message
    """
    name: str
    condition: str
    expected_value: Optional[Any] = None
    actual_value: Optional[Any] = None
    message: Optional[str] = None

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        """Validate name is not empty."""
        if not v or not v.strip():
            raise ValueError('name cannot be empty')
        return v.strip()

    @field_validator('condition')
    @classmethod
    def condition_not_empty(cls, v: str) -> str:
        """Validate condition is not empty."""
        if not v or not v.strip():
            raise ValueError('condition cannot be empty')
        return v.strip()


class TestResult(BaseModel):
    """
    Result of test execution.
    
    Attributes:
        success: Whether all tests passed
        passed_tests: Number of passed tests
        failed_tests: Number of failed tests
        skipped_tests: Number of skipped tests
        details: List of test result details
        duration_seconds: Test execution duration
        timestamp: Test execution timestamp
    """
    success: bool
    passed_tests: int = 0
    failed_tests: int = 0
    skipped_tests: int = 0
    details: List[Dict[str, Any]] = Field(default_factory=list)
    duration_seconds: float
    timestamp: datetime
    
    @field_validator('passed_tests', 'failed_tests', 'skipped_tests')
    @classmethod
    def counts_non_negative(cls, v: int) -> int:
        """Validate test counts are non-negative."""
        if v < 0:
            raise ValueError('test count must be non-negative')
        return v
    
    @field_validator('duration_seconds')
    @classmethod
    def duration_positive(cls, v: float) -> float:
        """Validate duration is non-negative."""
        if v < 0:
            raise ValueError('duration_seconds must be non-negative')
        return v


class PackageResult(BaseModel):
    """
    Result of platform packaging.
    
    Attributes:
        success: Whether packaging succeeded
        platform: Target platform
        output_path: Path to packaged output
        size_bytes: Package size in bytes
        duration_seconds: Packaging duration
        timestamp: Packaging timestamp
    """
    success: bool
    platform: str
    output_path: str
    size_bytes: int
    duration_seconds: float
    timestamp: datetime
    
    @field_validator('platform')
    @classmethod
    def platform_not_empty(cls, v: str) -> str:
        """Validate platform is not empty."""
        if not v or not v.strip():
            raise ValueError('platform cannot be empty')
        return v.strip()
    
    @field_validator('output_path')
    @classmethod
    def output_path_not_empty(cls, v: str) -> str:
        """Validate output_path is not empty."""
        if not v or not v.strip():
            raise ValueError('output_path cannot be empty')
        return v.strip()
    
    @field_validator('size_bytes')
    @classmethod
    def size_non_negative(cls, v: int) -> int:
        """Validate size is non-negative."""
        if v < 0:
            raise ValueError('size_bytes must be non-negative')
        return v
    
    @field_validator('duration_seconds')
    @classmethod
    def duration_positive(cls, v: float) -> float:
        """Validate duration is non-negative."""
        if v < 0:
            raise ValueError('duration_seconds must be non-negative')
        return v


# API Response Models (for file_manifest2.md completeness)

class ProjectResponse(BaseModel):
    """Response schema for project operations."""
    project_id: str
    project_name: str
    status: str
    created_at: datetime
    
    @field_validator('project_id', 'project_name', 'status')
    @classmethod
    def not_empty(cls, v: str) -> str:
        """Validate string fields are not empty."""
        if not v or not v.strip():
            raise ValueError(f'field cannot be empty')
        return v.strip()


class TaskResponse(BaseModel):
    """Response schema for async task operations."""
    task_id: str
    status: str
    message: str
    
    @field_validator('task_id', 'status', 'message')
    @classmethod
    def not_empty(cls, v: str) -> str:
        """Validate string fields are not empty."""
        if not v or not v.strip():
            raise ValueError(f'field cannot be empty')
        return v.strip()


class ProgressResponse(BaseModel):
    """Response schema for generation progress."""
    current_level: int
    total_levels: int
    critic_status: str
    files_generated: int
    
    @field_validator('critic_status')
    @classmethod
    def status_not_empty(cls, v: str) -> str:
        """Validate status is not empty."""
        if not v or not v.strip():
            raise ValueError('critic_status cannot be empty')
        return v.strip()
    
    @field_validator('current_level', 'total_levels', 'files_generated')
    @classmethod
    def counts_non_negative(cls, v: int) -> int:
        """Validate counts are non-negative."""
        if v < 0:
            raise ValueError('count must be non-negative')
        return v


class FileTreeResponse(BaseModel):
    """Response schema for file tree."""
    files: List[Dict[str, Any]]


class BuildStatusResponse(BaseModel):
    """Response schema for build status."""
    success: bool
    errors: List[ErrorReport] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    duration_seconds: float
    
    @field_validator('duration_seconds')
    @classmethod
    def duration_positive(cls, v: float) -> float:
        """Validate duration is non-negative."""
        if v < 0:
            raise ValueError('duration_seconds must be non-negative')
        return v


class CriticLogResponse(BaseModel):
    """Response schema for critic log."""
    phases: List[Dict[str, Any]]


class ValidationResult(BaseModel):
    """
    Result of Blueprint or test validation.

    Attributes:
        success: Whether validation succeeded
        errors: List of validation errors
        warnings: List of validation warnings
        validated_nodes: Number of nodes validated
        timestamp: Validation timestamp
    """
    success: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    validated_nodes: int = 0
    timestamp: datetime

    @field_validator('validated_nodes')
    @classmethod
    def nodes_non_negative(cls, v: int) -> int:
        """Validate validated_nodes is non-negative."""
        if v < 0:
            raise ValueError('validated_nodes must be non-negative')
        return v
