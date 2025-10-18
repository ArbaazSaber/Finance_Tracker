from pydantic import BaseModel, conint
from typing import Annotated, List, Optional


class BankColumnMapping(BaseModel):
    column_mapping_id: int
    bank_rule_id: int
    original_column: str
    mapped_column: str


class BankRule(BaseModel):
    bank_rule_id: int
    bank_id: int
    skiprows: Annotated[int, conint(ge=0)]
    skipfooter: Annotated[int, conint(ge=0)]
    usecols: str
    engine: str
    column_mapping: Optional[List[BankColumnMapping]] = None