from fastapi.routing import APIRouter

from sowonpass_backend.web.api import auth, docs, excel, monitoring, process_group, user
from sowonpass_backend.web.api import verification_history as history
from sowonpass_backend.web.api import verification_process as process
from sowonpass_backend.web.api import verify

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(process.router, prefix="/process", tags=["process"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(excel.router, prefix="/excel", tags=["excel"])
api_router.include_router(process_group.router, prefix="/group", tags=["group"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
api_router.include_router(verify.router, prefix="/verify", tags=["verify"])
