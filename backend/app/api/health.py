from datetime import UTC, datetime

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.core.config import settings
from app.services import registry

router = APIRouter(prefix="/api/v1/health", tags=["system"])
APP_STARTED_AT = datetime.now(UTC)


def _counts() -> dict[str, int]:
    return {
        "organizations": len(registry.db.organizations),
        "sites": len(registry.db.sites),
        "roles": len(registry.db.roles),
        "collaborators": len(registry.db.collaborators),
        "missions": len(registry.db.missions),
        "shifts": len(registry.db.shifts),
    }


@router.get("")
def healthcheck() -> dict[str, object]:
    return {
        "status": "ok",
        "version": settings.project_version,
        "project": settings.project_name,
        "started_at": APP_STARTED_AT.isoformat(),
        "timestamp": datetime.now(UTC).isoformat(),
        "dependencies": {
            "database": "ok",
        },
        "counts": _counts(),
    }


@router.get("/metrics", response_class=PlainTextResponse)
def metrics() -> str:
    lines = [
        "# HELP codex_entities_total Total number of in-memory entities.",
        "# TYPE codex_entities_total gauge",
    ]
    for key, value in _counts().items():
        lines.append(f'codex_entities_total{{entity="{key}"}} {value}')
    lines.extend(
        [
            "# HELP codex_app_info Static information about the application instance.",
            "# TYPE codex_app_info gauge",
            "codex_app_info{"
            f'project="{settings.project_name}",'  # noqa: ISC003
            f'version="{settings.project_version}"'  # noqa: ISC003
            "} 1",
            f'codex_app_uptime_seconds {int((datetime.now(UTC) - APP_STARTED_AT).total_seconds())}',
        ]
    )
    return "\n".join(lines)
