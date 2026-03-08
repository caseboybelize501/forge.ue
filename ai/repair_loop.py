"""
Repair Loop — Level 1 Core Agent

Parse UBT/UHT errors → Targeted file repair → Recompile.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.build_result (L0-004)
"""
from typing import List, Optional, Dict
from pathlib import Path

from contracts.models.game_brief import GameBrief
from contracts.models.build_result import CompileResult, ErrorReport, RepairContext


class RepairLoop:
    """
    Repair Loop for FORGE pipeline.

    Handles automated repair of UBT/UHT compilation errors:
    - Parses error messages
    - Classifies error types
    - Generates targeted fixes via LLM
    - Validates repairs
    - Max 3 attempts before HALT

    Attributes:
        max_attempts: Maximum repair attempts per file (default: 3)
    """

    MAX_REPAIR_ATTEMPTS = 3

    # UE5 Coding Standard Rules (injected into every repair prompt)
    UE5_CODING_RULES = """
    UE5 C++ rules:
    - UCLASS() before every UObject-derived class
    - GENERATED_BODY() after every UCLASS declaration
    - UPROPERTY() before every Blueprint-visible or replicated field
    - UFUNCTION() before every Blueprint-callable function
    - Never use raw pointers for UObject refs — use TObjectPtr<>
    - Never call delete on UObjects — use garbage collector
    - Platform-specific code MUST be wrapped in platform guards
    """

    # Error type patterns for classification
    ERROR_PATTERNS = {
        "missing_uclass": ["error C2143", "missing ';' before"],
        "missing_generated_body": ["unrecognized token", "expected ';'"],
        "missing_uproperty": ["property requires specifier"],
        "missing_ufunction": ["function requires specifier"],
        "include_error": ["fatal error C1083", "cannot open include file"],
        "linker_error": ["unresolved external symbol", "LNK2019", "LNK2001"],
        "syntax_error": ["syntax error", "C2059", "C2061"],
        "type_error": ["cannot convert", "C2440", "C2664"],
    }

    def __init__(self):
        """Initialize repair loop."""
        self.repair_history: Dict[str, List[str]] = {}

    def repair_file(self, context: RepairContext) -> Optional[str]:
        """
        Attempt to repair a failing file.

        Args:
            context: Repair context with error details

        Returns:
            Repaired file content, or None if max attempts exceeded
        """
        # Check if we've exceeded max attempts
        if len(context.prior_attempts) >= self.MAX_REPAIR_ATTEMPTS:
            return None
        
        # Classify the error type
        error_type = self.classify_error(context.error_text)
        
        # Build repair prompt for LLM
        repair_prompt = self._build_repair_prompt(context, error_type)
        
        # Generate repair (simulated - would call LLM in production)
        repaired_content = self._generate_repair(repair_prompt, context)
        
        # Validate the repair
        if self._validate_repair(repaired_content, context):
            return repaired_content
        
        return None

    def classify_error(self, error_text: str) -> str:
        """
        Classify UE5 build error type.

        Args:
            error_text: Raw error message from UBT/UHT

        Returns:
            Error classification string
        """
        error_lower = error_text.lower()
        
        for error_type, patterns in self.ERROR_PATTERNS.items():
            for pattern in patterns:
                if pattern.lower() in error_lower:
                    return error_type
        
        return "unknown"

    def _build_repair_prompt(self, context: RepairContext, error_type: str) -> str:
        """
        Build LLM prompt for repair.

        Args:
            context: Repair context
            error_type: Classified error type

        Returns:
            Formatted prompt for LLM
        """
        prompt = f"""
UE5 Code Repair Task
====================

Error Type: {error_type}
File: {context.failing_file}
Line: {context.error_line}
UE5 Version: {context.ue5_version}

Error Message:
{context.error_text}

Current File Content:
[File content would be here]

Prior Repair Attempts: {len(context.prior_attempts)}

{self.UE5_CODING_RULES}

Task: Generate the corrected code that fixes the error above.
Ensure all UE5 coding standards are followed.
"""
        return prompt

    def _generate_repair(self, prompt: str, context: RepairContext) -> str:
        """
        Generate repair using LLM (placeholder).

        Args:
            prompt: Repair prompt
            context: Repair context

        Returns:
            Generated repair content
        """
        # In production, this would call an LLM API
        # For now, return a placeholder
        return "// Repaired content placeholder"

    def _validate_repair(self, repaired_content: str, context: RepairContext) -> bool:
        """
        Validate that repair addresses the error.

        Args:
            repaired_content: Proposed fix
            context: Original repair context

        Returns:
            True if repair is valid
        """
        # Basic validation checks
        if not repaired_content or not repaired_content.strip():
            return False
        
        # Check for required UE5 macros based on error type
        error_type = self.classify_error(context.error_text)
        
        if error_type == "missing_uclass":
            if "UCLASS()" not in repaired_content:
                return False
        
        if error_type == "missing_generated_body":
            if "GENERATED_BODY()" not in repaired_content:
                return False
        
        if error_type == "missing_uproperty":
            if "UPROPERTY()" not in repaired_content:
                return False
        
        if error_type == "missing_ufunction":
            if "UFUNCTION()" not in repaired_content:
                return False
        
        return True

    def get_repair_statistics(self) -> Dict[str, int]:
        """
        Get repair statistics.

        Returns:
            Dictionary with repair statistics
        """
        total_attempts = sum(len(attempts) for attempts in self.repair_history.values())
        return {
            "total_files_repaired": len(self.repair_history),
            "total_repair_attempts": total_attempts,
            "average_attempts_per_file": total_attempts / len(self.repair_history) if self.repair_history else 0
        }
