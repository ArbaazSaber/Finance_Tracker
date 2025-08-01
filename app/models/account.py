from pydantic import BaseModel
from typing import Optional

class AccountBase(BaseModel):
    acc_name: str
    bank_name: str
    user_name: str

class AccountUpdate(BaseModel):
    acc_name: Optional[str]
    bank_name: Optional[str]