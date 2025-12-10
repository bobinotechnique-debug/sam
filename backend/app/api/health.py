from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/health", tags=["system"])


@router.get("")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
