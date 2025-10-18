from pydantic import BaseModel, StringConstraints
from typing import Annotated
class Bank(BaseModel):
    bank_id: int
    bank_name: Annotated[str, StringConstraints(min_length=1)]


class BankCreate(BaseModel):
    bank_name: Annotated[str, StringConstraints(min_length=1)]