from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum

class TransactionType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"

class Transaction(BaseModel):
    transaction_id: Optional[int] = None
    transaction_time: datetime
    description: Optional[str] = None
    old_description: Optional[str] = None
    amount: Decimal = Field(..., description="Amount must be negative for debits, positive for credits")
    reference_id: str = Field(..., min_length=1, description="Bank-provided unique transaction reference")
    type: TransactionType
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    tag_id: Optional[int] = None
    acc_id: Optional[int] = None
    user_id: Optional[int] = None

class TransactionUpsert(BaseModel):
    transaction_id: Optional[int]
    transaction_time: datetime
    description: Optional[str]
    old_description: str
    amount: float
    reference_id: str
    type: str
    created_at: Optional[datetime]
    modified_at: Optional[datetime]
    tag_name: str
    category_name: str
    acc_id: int
    user_name: str