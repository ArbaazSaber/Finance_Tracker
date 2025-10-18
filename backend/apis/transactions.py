from fastapi import APIRouter, HTTPException
from typing import List

from models.transaction import Transaction, TransactionUpsert, BulkTransactionRequest, BulkTransactionResponse
import services.transactions_service as transactions_service

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int):
    transaction = transactions_service.fetch_transaction_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.get("/user/{user_id}", response_model=List[Transaction])
def list_transactions_for_user(user_id: int):
    return transactions_service.get_all_transaction_for_user(user_id)


@router.get("/account/{acc_id}", response_model=List[Transaction])
def list_transactions_for_account(acc_id: int):
    return transactions_service.get_all_transaction_for_account(acc_id)

@router.post("/", response_model=int)
def create_transaction(transaction: Transaction):
    new_id = transactions_service.add_transaction(transaction)
    if not new_id:
        raise HTTPException(status_code=400, detail="Failed to insert transaction")
    return new_id

@router.put("/{transaction_id}")
def update_transaction(transaction_id: int, transaction: Transaction):
    success = transactions_service.modify_transaction(transaction_id, transaction)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update transaction")
    return {"status": "success"}

@router.post("/bulk", response_model=BulkTransactionResponse)
def bulk_create_transactions(request: BulkTransactionRequest):
    """
    Bulk insert multiple transactions.
    Returns detailed response with success/failure counts and any errors.
    """
    if not request.transactions:
        raise HTTPException(status_code=400, detail="No transactions provided")
    
    if len(request.transactions) > 1000:  # Limit bulk operations
        raise HTTPException(status_code=400, detail="Maximum 1000 transactions allowed per bulk operation")
    
    result = transactions_service.bulk_add_transactions(request.transactions)
    
    # If all transactions failed, return 400
    if result.success_count == 0 and result.failure_count > 0:
        raise HTTPException(status_code=400, detail=f"All {result.failure_count} transactions failed")
    
    return result
