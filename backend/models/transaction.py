from pydantic import BaseModel, Field
from typing import Optional, List
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
    
    def validate_amount_sign(self) -> 'Transaction':
        """Validate that amount sign matches transaction type"""
        if self.type == TransactionType.DEBIT and self.amount > 0:
            raise ValueError("Debit transactions must have negative amounts")
        elif self.type == TransactionType.CREDIT and self.amount <= 0:
            raise ValueError("Credit transactions must have positive amounts")
        return self


class TransactionUpsert(BaseModel):
    transaction_time: Optional[datetime] = None
    description: Optional[str] = None
    old_description: Optional[str] = None
    amount: Optional[Decimal] = None
    reference_id: Optional[str] = Field(None, min_length=1)
    type: Optional[TransactionType] = None
    tag_id: Optional[int] = None
    acc_id: Optional[int] = None
    user_id: Optional[int] = None


class BulkTransactionRequest(BaseModel):
    transactions: List[Transaction]


class BulkTransactionResponse(BaseModel):
    success_count: int
    failure_count: int
    total_processed: int
    inserted_ids: List[int]
    errors: Optional[List[str]] = None
