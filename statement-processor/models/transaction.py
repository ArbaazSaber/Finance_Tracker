from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from enum import Enum

class Transaction(BaseModel):
    transaction_id: Optional[int]
    transaction_time: datetime
    description: Optional[str]
    old_description: str
    amount: float
    reference_id: str
    type: str
    created_at: Optional[datetime]
    modified_at: Optional[datetime]
    tag_id: int
    category_id: int
    acc_id: int
    user_id: int

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