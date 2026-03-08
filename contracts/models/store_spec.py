"""
Store Specification Schema — Level 0 Foundation

Defines schemas for store submission assets and configuration.
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class StoreAssets(BaseModel):
    """Store submission assets."""
    screenshots: List[str]
    trailer_url: Optional[str]
    icon_path: str
    capsule_art: str
    description: str
    short_description: str


class RatingConfig(BaseModel):
    """ESRB/PEGI rating configuration."""
    rating_board: Literal["ESRB", "PEGI", "CERO"]
    content_descriptors: List[str]
    age_rating: str


class StoreSubmission(BaseModel):
    """Complete store submission package."""
    store: Literal["Steam", "EGS", "PSN", "Xbox", "Switch"]
    assets: StoreAssets
    rating: RatingConfig
    release_date: Optional[str]
    price_usd: Optional[float]
