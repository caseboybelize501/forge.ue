"""
FORGE Server API Package

REST API endpoints for FORGE platform.
"""
from server.api.projects import router as projects_router
from server.api.architecture import router as architecture_router
from server.api.generation import router as generation_router
from server.api.builds import router as builds_router
from server.api.packages import router as packages_router
from server.api.store import router as store_router
from server.api.auth import router as auth_router

__all__ = [
    'projects_router',
    'architecture_router',
    'generation_router',
    'builds_router',
    'packages_router',
    'store_router',
    'auth_router',
]
