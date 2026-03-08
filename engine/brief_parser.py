"""
Brief Parser — Level 2 Engine Module

Parse raw game brief → GameBrief schema via LLM.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.models.project_spec (L0-002)
- ai.architect_agent (L1-001)
"""
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import re

from contracts.models.game_brief import (
    GameBrief, Genre, Platform, MechanicSpec
)
from contracts.models.project_spec import ProjectSpec
from ai.architect_agent import ArchitectAgent


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

    # Genre keywords for detection
    GENRE_KEYWORDS = {
        Genre.ACTION: ['action', 'combat', 'fighting', 'shooter', 'hack'],
        Genre.RPG: ['rpg', 'role-playing', 'character progression', 'stats', 'leveling'],
        Genre.OPEN_WORLD: ['open world', 'sandbox', 'exploration', 'non-linear'],
        Genre.MULTIPLAYER: ['multiplayer', 'online', 'co-op', 'competitive', 'pvp'],
        Genre.MOBILE: ['mobile', 'casual', 'touch', 'ios', 'android'],
        Genre.PUZZLE: ['puzzle', 'logic', 'matching', 'brain teaser'],
        Genre.STRATEGY: ['strategy', 'rts', 'turn-based', 'tactical', 'management'],
    }

    # Platform keywords for detection
    PLATFORM_KEYWORDS = {
        Platform.PC: ['pc', 'windows', 'steam', 'epic'],
        Platform.MAC: ['mac', 'macos', 'osx'],
        Platform.ANDROID: ['android', 'google play'],
        Platform.IOS: ['ios', 'iphone', 'ipad', 'app store'],
        Platform.PS5: ['ps5', 'playstation 5', 'playstation5'],
        Platform.XBOX: ['xbox', 'xbox series', 'xbox one'],
        Platform.SWITCH: ['switch', 'nintendo switch'],
    }

    def __init__(self, architect: ArchitectAgent = None):
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
        # Extract title (first line or quoted text)
        title = self._extract_title(raw_brief)

        # Extract genre
        genre = self._extract_genre(raw_brief)

        # Extract platforms
        platforms = self._extract_platforms(raw_brief)

        # Extract mechanics
        mechanics = self._extract_mechanics(raw_brief)

        # Extract description
        description = self._extract_description(raw_brief)

        # Extract art style (optional)
        art_style = self._extract_art_style(raw_brief)

        # Create GameBrief
        brief = GameBrief(
            title=title,
            genre=genre,
            platforms=platforms,
            mechanics=mechanics,
            description=description,
            art_style=art_style
        )

        # Validate brief
        if not self.validate_brief(brief):
            raise ValueError("Parsed brief failed validation")

        return brief

    def validate_brief(self, brief: GameBrief) -> bool:
        """
        Validate brief completeness.

        Args:
            brief: Parsed game brief

        Returns:
            True if brief is complete and valid
        """
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            value = getattr(brief, field, None)
            if value is None:
                return False
            if isinstance(value, list) and len(value) == 0:
                return False
            if isinstance(value, str) and not value.strip():
                return False

        # Validate mechanics have valid priorities
        for mechanic in brief.mechanics:
            if mechanic.priority < 1 or mechanic.priority > 5:
                return False

        return True

    def _extract_title(self, text: str) -> str:
        """
        Extract title from text.

        Args:
            text: Brief text

        Returns:
            Extracted title
        """
        # Try to find quoted title first
        quoted_match = re.search(r'["\']([^"\']+)["\']', text)
        if quoted_match:
            return quoted_match.group(1).strip()

        # Try first line
        lines = text.strip().split('\n')
        if lines:
            first_line = lines[0].strip()
            # Remove common prefixes
            first_line = re.sub(r'^(title|game|project)[:\s]*', '', first_line, flags=re.IGNORECASE)
            if first_line:
                return first_line

        return "Untitled Game"

    def _extract_genre(self, text: str) -> Genre:
        """
        Extract genre from text.

        Args:
            text: Brief text

        Returns:
            Detected genre or Genre.ACTION as default
        """
        text_lower = text.lower()

        # Count keyword matches for each genre
        genre_scores: Dict[Genre, int] = {}

        for genre, keywords in self.GENRE_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                genre_scores[genre] = score

        # Return highest scoring genre
        if genre_scores:
            return max(genre_scores.keys(), key=lambda g: genre_scores[g])

        # Default to action
        return Genre.ACTION

    def _extract_platforms(self, text: str) -> List[Platform]:
        """
        Extract target platforms from text.

        Args:
            text: Brief text

        Returns:
            List of detected platforms
        """
        text_lower = text.lower()
        platforms: List[Platform] = []

        for platform, keywords in self.PLATFORM_KEYWORDS.items():
            if any(keyword in text_lower for keyword in keywords):
                platforms.append(platform)

        # Default to PC if no platforms detected
        if not platforms:
            platforms.append(Platform.PC)

        return platforms

    def _extract_mechanics(self, text: str) -> List[MechanicSpec]:
        """
        Extract game mechanics from text.

        Args:
            text: Brief text

        Returns:
            List of mechanic specifications
        """
        mechanics: List[MechanicSpec] = []

        # Look for bullet points or numbered lists
        lines = text.split('\n')

        mechanic_patterns = [
            r'[-*•]\s*(.+?)(?:\s*[-–—]\s*(.+?))?$',  # Bullet points
            r'\d+\.\s*(.+?)(?:\s*[-–—]\s*(.+?))?$',  # Numbered lists
            r'mechanic[:\s]+(.+)$',  # "Mechanic: description"
        ]

        priority = 1
        for line in lines:
            line = line.strip()

            for pattern in mechanic_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    name = match.group(1).strip() if match.group(1) else ''
                    description = match.group(2).strip() if match.group(2) else name

                    if name and len(name) > 2:  # Filter out very short matches
                        mechanics.append(MechanicSpec(
                            name=name,
                            description=description,
                            priority=min(priority, 5)
                        ))
                        priority += 1
                    break

        # If no mechanics found, create a default one
        if not mechanics:
            mechanics.append(MechanicSpec(
                name="Core Gameplay",
                description="Basic game interaction",
                priority=5
            ))

        return mechanics

    def _extract_description(self, text: str) -> str:
        """
        Extract main description from text.

        Args:
            text: Brief text

        Returns:
            Extracted description
        """
        # Remove title line if present
        lines = text.split('\n')

        # Find description section
        description_start = 0
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            if any(marker in line_lower for marker in ['description', 'overview', 'summary', 'about']):
                description_start = i + 1
                break

        # Extract description lines
        description_lines = []
        for line in lines[description_start:]:
            line = line.strip()
            # Skip empty lines at start
            if not line and not description_lines:
                continue
            # Skip section headers
            if line.startswith('#') or line.startswith('='):
                if description_lines:
                    break
                continue
            description_lines.append(line)

        description = '\n'.join(description_lines)

        # If no description found, use first paragraph
        if not description.strip():
            # Find first substantial paragraph
            for line in lines:
                line = line.strip()
                if len(line) > 50 and not line.startswith('#'):
                    description = line
                    break

        return description.strip() or "A game experience."

    def _extract_art_style(self, text: str) -> Optional[str]:
        """
        Extract art style notes from text.

        Args:
            text: Brief text

        Returns:
            Art style description or None
        """
        text_lower = text.lower()

        # Look for art style section
        art_patterns = [
            r'art style[:\s]+(.+?)(?=\n\n|\n#|\Z)',
            r'art direction[:\s]+(.+?)(?=\n\n|\n#|\Z)',
            r'visual style[:\s]+(.+?)(?=\n\n|\n#|\Z)',
            r'aesthetic[:\s]+(.+?)(?=\n\n|\n#|\Z)',
        ]

        for pattern in art_patterns:
            match = re.search(pattern, text_lower)
            if match:
                # Get original case from text
                start = match.start(1)
                end = match.end(1)
                return text[start:end].strip()

        # Look for art style keywords
        art_keywords = ['pixel art', 'realistic', 'stylized', 'cartoon', 'low poly',
                       'hand-drawn', '3d', '2d', 'retro', 'modern']

        found_keywords = []
        for keyword in art_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)

        if found_keywords:
            return ', '.join(found_keywords).title()

        return None

    def parse_and_design(self, raw_brief: str, templates_dir: Path) -> Tuple[GameBrief, ProjectSpec]:
        """
        Parse brief and generate architecture.

        Args:
            raw_brief: Raw game brief text
            templates_dir: Path to templates directory

        Returns:
            Tuple of (GameBrief, ProjectSpec)
        """
        # Parse brief
        brief = self.parse_brief(raw_brief)

        # Generate architecture if architect is available
        if self.architect is None:
            self.architect = ArchitectAgent(templates_dir)

        project_spec = self.architect.design_architecture(brief)

        return brief, project_spec
