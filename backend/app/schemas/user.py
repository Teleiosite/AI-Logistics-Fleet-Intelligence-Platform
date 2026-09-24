from pydantic import BaseModel


class UserRead(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool

    model_config = {"from_attributes": True}
