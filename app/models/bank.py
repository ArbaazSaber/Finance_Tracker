from pydantic import BaseModel

class BankCreate(BaseModel):
    bank_name: str