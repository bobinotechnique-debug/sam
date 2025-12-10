from fastapi import APIRouter

from app.api.collaborators import router as collaborators_router
from app.api.health import router as health_router
from app.api.missions import router as missions_router
from app.api.organizations import router as organizations_router
from app.api.planning import router as planning_router
from app.api.roles import router as roles_router
from app.api.shifts import router as shifts_router
from app.api.sites import router as sites_router

router = APIRouter()
router.include_router(health_router)
router.include_router(organizations_router)
router.include_router(sites_router)
router.include_router(roles_router)
router.include_router(collaborators_router)
router.include_router(missions_router)
router.include_router(shifts_router)
router.include_router(planning_router)
