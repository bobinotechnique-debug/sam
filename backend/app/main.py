from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.logging import configure_logging, logger


def create_application() -> FastAPI:
    configure_logging()
    application = FastAPI(title=settings.project_name)
    application.include_router(router)
    logger.info("Application created", extra={"project_name": settings.project_name})
    return application


app = create_application()
