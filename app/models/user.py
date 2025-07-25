from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserAuth(BaseModel):
    username_or_email: str
    password: str

class UserPasswordUpdateRequest(BaseModel):
    new_password: str = Field(..., min_length=8, example="MyStrongPass123")
