from pydantic import BaseModel, Field


class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    slug: str = Field(min_length=2, max_length=100)
    timezone: str = "Africa/Lagos"


class CompanyRead(CompanyCreate):
    id: str
    subscription_tier: str
    is_active: bool

    model_config = {"from_attributes": True}
