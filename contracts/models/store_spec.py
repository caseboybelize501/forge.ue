"""
Store Specification Schema — Level 0 Foundation

Defines schemas for store submission assets and configuration.

Dependencies: None (foundation file)
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class StorePlatform(str, Enum):
    """
    Store platform enumeration.
    
    Supported digital distribution platforms.
    """
    STEAM = "Steam"
    EGS = "EGS"
    PSN = "PSN"
    XBOX = "Xbox"
    SWITCH = "Switch"


class RatingBoard(str, Enum):
    """
    Rating board enumeration.
    
    Regional game rating authorities.
    """
    ESRB = "ESRB"
    PEGI = "PEGI"
    CERO = "CERO"


class StoreAssets(BaseModel):
    """
    Store submission assets.
    
    Attributes:
        screenshots: List of screenshot file paths
        trailer_url: Optional trailer video URL
        icon_path: Path to store icon image
        capsule_art: Path to capsule art image
        description: Full store description
        short_description: Short description for listings
    """
    screenshots: List[str]
    trailer_url: Optional[str] = None
    icon_path: str
    capsule_art: str
    description: str
    short_description: str
    
    @field_validator('screenshots')
    @classmethod
    def at_least_one_screenshot(cls, v: List[str]) -> List[str]:
        """Validate at least one screenshot."""
        if not v or len(v) == 0:
            raise ValueError('at least one screenshot is required')
        return v
    
    @field_validator('icon_path')
    @classmethod
    def icon_path_not_empty(cls, v: str) -> str:
        """Validate icon path is not empty."""
        if not v or not v.strip():
            raise ValueError('icon_path cannot be empty')
        return v.strip()
    
    @field_validator('capsule_art')
    @classmethod
    def capsule_art_not_empty(cls, v: str) -> str:
        """Validate capsule art path is not empty."""
        if not v or not v.strip():
            raise ValueError('capsule_art cannot be empty')
        return v.strip()
    
    @field_validator('description')
    @classmethod
    def description_not_empty(cls, v: str) -> str:
        """Validate description is not empty."""
        if not v or not v.strip():
            raise ValueError('description cannot be empty')
        return v.strip()
    
    @field_validator('short_description')
    @classmethod
    def short_description_not_empty(cls, v: str) -> str:
        """Validate short description is not empty."""
        if not v or not v.strip():
            raise ValueError('short_description cannot be empty')
        return v.strip()


class RatingConfig(BaseModel):
    """
    ESRB/PEGI rating configuration.
    
    Attributes:
        rating_board: Rating authority (ESRB, PEGI, CERO)
        content_descriptors: List of content descriptors
        age_rating: Age rating string (e.g., "M", "18", "C")
    """
    rating_board: RatingBoard
    content_descriptors: List[str]
    age_rating: str
    
    @field_validator('content_descriptors')
    @classmethod
    def at_least_one_descriptor(cls, v: List[str]) -> List[str]:
        """Validate at least one content descriptor."""
        if not v or len(v) == 0:
            raise ValueError('at least one content descriptor is required')
        return v
    
    @field_validator('age_rating')
    @classmethod
    def age_rating_not_empty(cls, v: str) -> str:
        """Validate age rating is not empty."""
        if not v or not v.strip():
            raise ValueError('age_rating cannot be empty')
        return v.strip()


class StoreSubmission(BaseModel):
    """
    Complete store submission package.
    
    Attributes:
        store: Target store platform
        assets: Store assets
        rating: Rating configuration
        release_date: Optional release date (YYYY-MM-DD)
        price_usd: Optional price in USD
    """
    store: StorePlatform
    assets: StoreAssets
    rating: RatingConfig
    release_date: Optional[str] = None
    price_usd: Optional[float] = None
    
    @field_validator('release_date')
    @classmethod
    def release_date_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate release date format (YYYY-MM-DD)."""
        if v:
            import re
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
                raise ValueError('release_date must be in YYYY-MM-DD format')
        return v
    
    @field_validator('price_usd')
    @classmethod
    def price_positive(cls, v: Optional[float]) -> Optional[float]:
        """Validate price is non-negative."""
        if v is not None and v < 0:
            raise ValueError('price_usd must be non-negative')
        return v
