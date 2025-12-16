from datetime import UTC, datetime
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import RequestResponseEndpoint

from app.api.errors import register_exception_handlers
from app.api.routes import router
from app.core.config import settings
from app.core.logging import TRACE_ID_CTX, configure_logging, logger


def create_application() -> FastAPI:
    configure_logging()
    application = FastAPI(title=settings.project_name)

    cors_allowed_origins = list(settings.cors_origins)
    allow_origin_regex = None

    if "*" in cors_allowed_origins:
        cors_allowed_origins = []
        allow_origin_regex = ".*"

    application.add_middleware(
        CORSMiddleware,
        allow_origins=cors_allowed_origins,
        allow_origin_regex=allow_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.middleware("http")
    async def add_request_trace_id(
        request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        trace_id = str(uuid4())
        token = TRACE_ID_CTX.set(trace_id)
        request.state.trace_id = trace_id
        try:
            response = await call_next(request)
        finally:
            TRACE_ID_CTX.reset(token)
        response.headers.setdefault("X-Request-ID", trace_id)
        return response

    @application.middleware("http")
    async def stamp_response_time(request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        response.headers.setdefault("X-App-Timestamp", datetime.now(UTC).isoformat())
        return response

    @application.get("/", include_in_schema=False, response_class=JSONResponse)
    async def root() -> dict[str, str]:
        return {
            "message": "Backend API is running.",
            "docs_url": "/docs",
            "health_url": "/api/v1/health",
        }

    register_exception_handlers(application)
    application.include_router(router)
    logger.info("Application created", extra={"project_name": settings.project_name})
    return application


app = create_application()
