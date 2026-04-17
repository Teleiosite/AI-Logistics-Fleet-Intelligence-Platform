from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.schemas.company import CompanyCreate, CompanyRead
from app.services.crud import create_company, list_companies

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def create_company_endpoint(payload: CompanyCreate, db: Session = Depends(get_db)) -> CompanyRead:
    try:
        entity = create_company(db, payload)
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail="Company slug must be unique") from exc
    return CompanyRead.model_validate(entity)


@router.get("", response_model=list[CompanyRead])
def list_companies_endpoint(
    db: Session = Depends(get_db), auth: AuthContext = Depends(require_permission("companies", "read"))
) -> list[CompanyRead]:
    if auth.role not in {"super_admin", "company_admin"}:
        raise HTTPException(status_code=403, detail="Only admins can list companies")
    return [CompanyRead.model_validate(company) for company in list_companies(db)]
