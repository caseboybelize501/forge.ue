"""
FORGE Server Main — Level 8 Entry Point

FastAPI application entry point.

Dependencies:
- server.api.projects (L7-001)
- server.api.architecture (L7-002)
- server.api.generation (L7-003)
- server.api.builds (L7-004)
- server.api.packages (L7-005)
- server.api.store (L7-006)
- server.api.auth (L7-007)
- server.workers.generation_worker (L7-008)
- server.workers.build_worker (L7-009)
- server.workers.package_worker (L7-010)
- server.models (L7-014)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
import os

from server.api.projects import router as projects_router
from server.api.architecture import router as architecture_router
from server.api.generation import router as generation_router
from server.api.builds import router as builds_router
from server.api.packages import router as packages_router
from server.api.store import router as store_router
from server.api.auth import router as auth_router
from server.workers.generation_worker import app as celery_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup + shutdown lifecycle.
    
    Yields:
        None
    """
    # Startup
    os.environ.setdefault("UNREAL_ENGINE_ROOT", os.getenv("UNREAL_ENGINE_ROOT", ""))
    yield
    # Shutdown
    celery_app.close()


app = FastAPI(
    title="FORGE API",
    description="Autonomous Unreal Engine 5 Game Development Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects_router)
app.include_router(architecture_router)
app.include_router(generation_router)
app.include_router(builds_router)
app.include_router(packages_router)
app.include_router(store_router)
app.include_router(auth_router)


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
