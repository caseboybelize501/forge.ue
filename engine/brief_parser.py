"""
Brief Parser — Level 2 Engine Module

Parse raw game brief → GameBrief schema via LLM.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- ai.architect_agent (L1-001)
"""
from typing import Optional, Dict, Any
from pathlib import Path

from contracts.models.game_brief import GameBrief, Genre, Platform, MechanicSpec
from contracts.models.project_spec import ProjectSpec


class BriefParser:
    """
    Game Brief Parser.
    
    Uses LLM to extract structured GameBrief from raw text:
    - Identifies genre from description
    - Extracts target platforms
    - Parses mechanics list
    - Validates completeness
    
    Attributes:
        architect: Reference to architect agent for validation
    """
    
    # Required fields for valid brief
    REQUIRED_FIELDS = ['title', 'genre', 'platforms', 'description']
    
    def __init__(self, architect=None):
        """
        Initialize brief parser.
        
        Args:
            architect: Optional architect agent for validation
        """
        self.architect = architect
    
    def parse_brief(self, raw_brief: str) -> GameBrief:
        """
        Extract structured GameBrief from raw text.
        
        Args:
            raw_brief: Raw game brief text
            
        Returns:
            Parsed GameBrief schema
        """
        pass
    
    def validate_brief(self, brief: GameBrief) -> bool:
        """
        Validate brief completeness.
        
        Args:
            brief: Parsed game brief
            
        Returns:
            True if brief is complete and valid
        """
        pass
    
    def _extract_genre(self, text: str) -> Optional[Genre]:
        """
        Extract genre from text.
        
        Args:
            text: Brief text
            
        Returns:
            Detected genre or None
        """
        pass
    
    def _extract_platforms(self, text: str) -> List[Platform]:
        """
        Extract target platforms from text.
        
        Args:
            text: Brief text
            
        Returns:
            List of detected platforms
        """
        pass
    
    def _extract_mechanics(self, text: str) -> List[MechanicSpec]:
        """
        Extract game mechanics from text.
        
        Args:
            text: Brief text
            
        Returns:
            List of mechanic specifications
        """
        pass
