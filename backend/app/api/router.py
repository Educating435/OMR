from fastapi import APIRouter

from app.modules.answer_keys.router import router as answer_keys_router
from app.modules.auth.router import router as auth_router
from app.modules.exams.router import router as exams_router
from app.modules.exports.router import router as exports_router
from app.modules.results.router import router as results_router
from app.modules.templates.router import router as templates_router
from app.modules.users.router import router as users_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(exams_router, prefix="/exams", tags=["exams"])
api_router.include_router(answer_keys_router, prefix="/answer-keys", tags=["answer-keys"])
api_router.include_router(templates_router, prefix="/templates", tags=["templates"])
api_router.include_router(results_router, prefix="/results", tags=["results"])
api_router.include_router(exports_router, prefix="/exports", tags=["exports"])


@api_router.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": "render-api",
        "database": "hostinger-mysql",
    }
