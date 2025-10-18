from pydantic import BaseModel
from typing import List


class BankColumn(BaseModel):
    bank_rule_id: int
    original_column: str
    mapped_column: str

class BankRule(BaseModel):
    bank_rule_id: int
    bank_id: int
    skiprows: int
    skipfooter: int
    usecols: str
    engine: str
    column_mapping: List[BankColumn]