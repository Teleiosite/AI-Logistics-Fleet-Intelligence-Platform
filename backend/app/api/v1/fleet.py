from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.schemas.fleet import (
    DriverCreate,
    DriverRead,
    TransporterCreate,
    TransporterRead,
    VehicleCreate,
    VehicleRead,
)
from app.services.crud import (
    create_driver,
    create_transporter,
    create_vehicle,
    list_drivers,
    list_transporters,
    list_vehicles,
)

router = APIRouter(tags=["fleet"])


@router.post("/vehicles", response_model=VehicleRead, status_code=status.HTTP_201_CREATED)
def create_vehicle_endpoint(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fleet", "write")),
) -> VehicleRead:
    try:
        vehicle = create_vehicle(db, auth.company_id, payload)
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail="Duplicate license plate") from exc
    return VehicleRead.model_validate(vehicle)


@router.get("/vehicles", response_model=list[VehicleRead])
def list_vehicles_endpoint(
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fleet", "read")),
) -> list[VehicleRead]:
    return [VehicleRead.model_validate(item) for item in list_vehicles(db, auth.company_id)]


@router.post("/drivers", response_model=DriverRead, status_code=status.HTTP_201_CREATED)
def create_driver_endpoint(
    payload: DriverCreate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fleet", "write")),
) -> DriverRead:
    try:
        driver = create_driver(db, auth.company_id, payload)
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail="Duplicate driver license") from exc
    return DriverRead.model_validate(driver)


@router.get("/drivers", response_model=list[DriverRead])
def list_drivers_endpoint(
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fleet", "read")),
) -> list[DriverRead]:
    return [DriverRead.model_validate(item) for item in list_drivers(db, auth.company_id)]


@router.post("/transporters", response_model=TransporterRead, status_code=status.HTTP_201_CREATED)
def create_transporter_endpoint(
    payload: TransporterCreate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fleet", "write")),
) -> TransporterRead:
    transporter = create_transporter(db, auth.company_id, payload)
    return TransporterRead.model_validate(transporter)


@router.get("/transporters", response_model=list[TransporterRead])
def list_transporters_endpoint(
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fleet", "read")),
) -> list[TransporterRead]:
    return [TransporterRead.model_validate(item) for item in list_transporters(db, auth.company_id)]
