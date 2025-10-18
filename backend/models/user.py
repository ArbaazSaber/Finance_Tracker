from pydantic import BaseModel, StringConstraints
from typing import Optional, Annotated
from datetime import datetime

class User(BaseModel):
    user_id: int
    username: Annotated[str, StringConstraints(min_length=1)]
    # Use plain str here to avoid requiring the optional 'email-validator' package at import time
    email: str
    password_hash: str
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    is_active: bool = True


class UserCreate(BaseModel):
    username: Annotated[str, StringConstraints(min_length=1)]
    email: str
    password: str


class UserAuth(BaseModel):
    username_or_email: str
    password: str


class UserPasswordUpdateRequest(BaseModel):
    password: str
