from fastapi import APIRouter

from app.api.v1.ai import router as ai_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.auth import router as auth_router
from app.api.v1.companies import router as companies_router
from app.api.v1.dvr import router as dvr_router
from app.api.v1.fleet import router as fleet_router
from app.api.v1.fuel import router as fuel_router
from app.api.v1.health import router as health_router
from app.api.v1.invoices import router as invoices_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.shipments import router as shipments_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(companies_router)
api_router.include_router(fleet_router)
api_router.include_router(shipments_router)
api_router.include_router(fuel_router)
api_router.include_router(dvr_router)
api_router.include_router(invoices_router)
api_router.include_router(analytics_router)
api_router.include_router(ai_router)
api_router.include_router(notifications_router)
