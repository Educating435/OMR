from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import routes_auth, routes_exams, routes_exports, routes_health, routes_results, routes_templates, routes_users
from app.core.config import settings
from app.core.database import Base, engine
from app.core.logging import configure_logging
import app.models  # noqa: F401


configure_logging()

app = FastAPI(title=settings.app_name)


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_code": "http_error"},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc) if settings.debug else "Internal server error", "error_code": "internal_error"},
    )


if settings.debug or settings.auto_create_schema:
    Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_health.router, prefix=settings.api_v1_prefix, tags=["health"])
app.include_router(routes_auth.router, prefix=settings.api_v1_prefix, tags=["auth"])
app.include_router(routes_users.router, prefix=settings.api_v1_prefix, tags=["users"])
app.include_router(routes_exams.router, prefix=settings.api_v1_prefix, tags=["exams"])
app.include_router(routes_templates.router, prefix=settings.api_v1_prefix, tags=["templates"])
app.include_router(routes_results.router, prefix=settings.api_v1_prefix, tags=["results"])
app.include_router(routes_exports.router, prefix=settings.api_v1_prefix, tags=["exports"])
