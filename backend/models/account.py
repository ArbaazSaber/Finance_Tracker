from pydantic import BaseModel, Field
from typing import Optional, Annotated
from pydantic import StringConstraints


class Account(BaseModel):
    acc_id: int
    acc_name: Annotated[str, StringConstraints(min_length=1)]
    user_id: int
    bank_id: int
    is_active: bool = True
    balance: int
    currency: str


class AccountBase(BaseModel):
    """Model used for creating an account from API input.

    NOTE: creation expects user and bank by name (strings) so callers can pass
    human-readable values instead of DB ids.
    """
    acc_name: str = Field(..., min_length=1)
    bank_name: str = Field(..., min_length=1)
    user_name: str = Field(..., min_length=1)
    balance: int = Field(default=0)
    currency: str = Field(min_length=3, max_length=3)


class AccountUpdate(BaseModel):
    """Partial model for updating an account. Fields are optional."""
    acc_name: Optional[str] = None
    bank_name: Optional[str] = None
    balance: Optional[int] = None
    currency: Optional[str] = None
