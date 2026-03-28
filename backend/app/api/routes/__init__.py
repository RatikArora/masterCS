from app.api.routes.auth import router as auth_router
from app.api.routes.concepts import router as concepts_router
from app.api.routes.learning import router as learning_router
from app.api.routes.progress import router as progress_router
from app.api.routes.badges import router as badges_router

__all__ = ["auth_router", "concepts_router", "learning_router", "progress_router", "badges_router"]