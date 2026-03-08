"""
Game Brief Schema — Level 0 Foundation

Defines the input schema for game briefs submitted to FORGE.
Immutable after Step 0 human review.
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Genre(str, Enum):
    """Supported game genres."""
    ACTION = "action"
    RPG = "rpg"
    OPEN_WORLD = "open_world"
    MULTIPLAYER = "multiplayer"
    MOBILE = "mobile"
    PUZZLE = "puzzle"
    STRATEGY = "strategy"


class Platform(str, Enum):
    """Target deployment platforms."""
    PC = "pc"
    MAC = "mac"
    ANDROID = "android"
    IOS = "ios"
    PS5 = "ps5"
    XBOX = "xbox"
    SWITCH = "switch"


class MechanicSpec(BaseModel):
    """Specification for a game mechanic."""
    name: str
    description: str
    priority: int = Field(ge=1, le=5)


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
