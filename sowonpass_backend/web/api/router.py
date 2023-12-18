from fastapi.routing import APIRouter

from sowonpass_backend.web.api import auth, docs, echo, monitoring, user
from sowonpass_backend.web.api import verification_process as process

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(process.router, prefix="/process", tags=["process"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
