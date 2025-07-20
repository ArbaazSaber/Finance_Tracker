from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserAuth(BaseModel):
    username_or_email: str
    password: str