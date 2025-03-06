from fastapi import APIRouter
from .incidents import router as incidents_router
from .notifications import router as notifications_router

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(incidents_router)
router.include_router(notifications_router)

@router.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
