from pydantic import BaseModel, EmailStr
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    model_config = {"from_attributes": True}
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
