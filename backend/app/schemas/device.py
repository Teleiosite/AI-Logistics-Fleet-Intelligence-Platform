from pydantic import BaseModel, Field


class DeviceTokenCreate(BaseModel):
    token: str = Field(min_length=16, max_length=512)
    platform: str = Field(pattern="^(ios|android|web)$")
