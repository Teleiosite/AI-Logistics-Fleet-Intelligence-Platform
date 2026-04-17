from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    company_id: str
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str
    last_name: str
    role: str = "company_admin"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserContextResponse(BaseModel):
    email: str
    company_id: str
    role: str
