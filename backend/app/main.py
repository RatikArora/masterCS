from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db.base import Base
from app.db.session import engine
from app.api.routes import auth_router, concepts_router, learning_router, progress_router

# Import all models so they register with Base.metadata
import app.models  # noqa: F401

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Adaptive CS Learning System with Spaced Repetition",
    )

    # CORS — allow frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Register routers
    app.include_router(auth_router, prefix="/api")
    app.include_router(concepts_router, prefix="/api")
    app.include_router(learning_router, prefix="/api")
    app.include_router(progress_router, prefix="/api")

    @app.get("/api/health")
    def health_check():
        return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}

    return app


app = create_app()
