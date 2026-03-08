"""
Game Brief Schema — Level 0 Foundation

Defines the input schema for game briefs submitted to FORGE.
Immutable after Step 0 human review.

Dependencies: None (foundation file)
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class Genre(str, Enum):
    """Supported game genres per forgeue.md."""
    ACTION = "action"
    RPG = "rpg"
    OPEN_WORLD = "open_world"
    MULTIPLAYER = "multiplayer"
    MOBILE = "mobile"
    PUZZLE = "puzzle"
    STRATEGY = "strategy"


class Platform(str, Enum):
    """Target deployment platforms per forgeue.md."""
    PC = "pc"
    MAC = "mac"
    ANDROID = "android"
    IOS = "ios"
    PS5 = "ps5"
    XBOX = "xbox"
    SWITCH = "switch"


class MechanicSpec(BaseModel):
    """
    Specification for a game mechanic.
    
    Attributes:
        name: Mechanic name
        description: Mechanic description
        priority: Priority level (1-5, 5 being highest)
    """
    name: str
    description: str
    priority: int = Field(ge=1, le=5, description="Priority level 1-5")
    
    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        """Validate name is not empty."""
        if not v or not v.strip():
            raise ValueError('name cannot be empty')
        return v.strip()
    
    @field_validator('description')
    @classmethod
    def description_not_empty(cls, v: str) -> str:
        """Validate description is not empty."""
        if not v or not v.strip():
            raise ValueError('description cannot be empty')
        return v.strip()


class GameBrief(BaseModel):
    """
    Input schema for game briefs.
    
    Attributes:
        title: Project title
        genre: Primary game genre
        platforms: Target deployment platforms
        mechanics: List of game mechanics
        description: High-level game description
        art_style: Art direction notes
    """
    title: str
    genre: Genre
    platforms: List[Platform]
    mechanics: List[MechanicSpec]
    description: str
    art_style: Optional[str] = None
    
    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty."""
        if not v or not v.strip():
            raise ValueError('title cannot be empty')
        return v.strip()
    
    @field_validator('description')
    @classmethod
    def description_not_empty(cls, v: str) -> str:
        """Validate description is not empty."""
        if not v or not v.strip():
            raise ValueError('description cannot be empty')
        return v.strip()
    
    @field_validator('platforms')
    @classmethod
    def at_least_one_platform(cls, v: List[Platform]) -> List[Platform]:
        """Validate at least one platform is specified."""
        if not v or len(v) == 0:
            raise ValueError('at least one platform must be specified')
        return v
    
    @field_validator('mechanics')
    @classmethod
    def at_least_one_mechanic(cls, v: List[MechanicSpec]) -> List[MechanicSpec]:
        """Validate at least one mechanic is specified."""
        if not v or len(v) == 0:
            raise ValueError('at least one mechanic must be specified')
        return v


class GameBriefRequest(BaseModel):
    """
    Request schema for creating a project via API.
    
    Attributes:
        brief: Raw game brief text
    """
    brief: str
    
    @field_validator('brief')
    @classmethod
    def brief_not_empty(cls, v: str) -> str:
        """Validate brief is not empty."""
        if not v or not v.strip():
            raise ValueError('brief cannot be empty')
        return v.strip()
