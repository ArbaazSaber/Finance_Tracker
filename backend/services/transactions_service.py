from typing import List, Optional

from utils.logger import logger
from models.transaction import Transaction, TransactionUpsert, BulkTransactionResponse, TransactionType

import repositories.transactions_repository as transactions_repo
import repositories.tags_repository as tags_repo
import repositories.categories_repository as categories_repository
import repositories.users_repository as user_repo
import repositories.accounts_repository as accounts_repository


def fetch_transaction_by_id(transaction_id: int) -> Optional[Transaction]:
    if transaction_id <= 0:
        logger.warning(f"Invalid transaction_id: {transaction_id}")
        return None
    return transactions_repo.get_transaction_by_id(transaction_id)

def get_all_transaction_for_user(user_id: int) -> List[Transaction]:
    if user_id <= 0:
        logger.warning(f"Invalid user_id: {user_id}")
        return []
    return transactions_repo.get_all_transaction_for_user(user_id)

def get_all_transaction_for_account(acc_id: int) -> List[Transaction]:
    if acc_id <= 0:
        logger.warning(f"Invalid acc_id: {acc_id}")
        return []
    return transactions_repo.get_all_transaction_for_account(acc_id)

def _validate_transaction_amount_sign(transaction: Transaction) -> bool:
    """Validate that transaction amount sign matches the transaction type"""
    if transaction.type == TransactionType.DEBIT and transaction.amount > 0:
        logger.warning(f"Debit transaction has positive amount: {transaction.amount}")
        return False
    elif transaction.type == TransactionType.CREDIT and transaction.amount <= 0:
        logger.warning(f"Credit transaction has non-positive amount: {transaction.amount}")
        return False
    return True

def add_transaction(transaction: Transaction) -> Optional[int]:
    if not transaction.user_id or not transaction.acc_id:
        logger.warning("Transaction must include user_id and acc_id")
        return None
    
    if not _validate_transaction_amount_sign(transaction):
        logger.warning("Transaction amount sign validation failed")
        return None
        
    return transactions_repo.insert_transaction(transaction)

def modify_transaction(transaction_id: int, new_data: Transaction) -> bool:
    if transaction_id <= 0:
        logger.warning(f"Invalid transaction_id: {transaction_id}")
        return False

    existing = transactions_repo.get_transaction_by_id(transaction_id)
    if not existing:
        logger.warning(f"No transaction found with id: {transaction_id}")
        return False

    # Merge non-None fields from new_data into existing
    updated = Transaction(
        transaction_id=None,
        transaction_time=new_data.transaction_time or existing.transaction_time,
        description=new_data.description or existing.description,
        old_description=new_data.old_description or existing.old_description,
        amount=new_data.amount if new_data.amount is not None else existing.amount,
        reference_id=new_data.reference_id or existing.reference_id,
        type=new_data.type or existing.type,
        tag_id=new_data.tag_id or existing.tag_id,
        created_at=None,
        modified_at=None,
        acc_id=new_data.acc_id or existing.acc_id,
        user_id=new_data.user_id or existing.user_id
    )
    
    # Validate amount sign if type or amount changed
    if new_data.type or new_data.amount is not None:
        if not _validate_transaction_amount_sign(updated):
            logger.warning("Transaction update failed amount sign validation")
            return False

    return transactions_repo.update_transaction(transaction_id, updated)

def bulk_add_transactions(transactions: List[Transaction]) -> BulkTransactionResponse:
    """
    Bulk insert multiple transactions with validation and error handling.
    Returns a BulkTransactionResponse with success/failure counts and details.
    """
    if not transactions:
        logger.warning("Empty transactions list provided for bulk insert")
        return BulkTransactionResponse(
            success_count=0,
            failure_count=0,
            total_processed=0,
            inserted_ids=[],
            errors=["No transactions provided"]
        )
    
    # Pre-validate transactions
    valid_transactions = []
    pre_validation_errors = []
    
    for i, transaction in enumerate(transactions):
        if not transaction.user_id or not transaction.acc_id:
            pre_validation_errors.append(f"Transaction {i}: Missing required user_id or acc_id")
            continue
        
        if not transaction.transaction_time:
            pre_validation_errors.append(f"Transaction {i}: Missing required transaction_time")
            continue
            
        if transaction.amount is None:
            pre_validation_errors.append(f"Transaction {i}: Missing required amount")
            continue
        
        if not transaction.reference_id:
            pre_validation_errors.append(f"Transaction {i}: Missing required reference_id")
            continue
            
        if not _validate_transaction_amount_sign(transaction):
            pre_validation_errors.append(f"Transaction {i}: Amount sign doesn't match transaction type")
            continue
            
        valid_transactions.append(transaction)
    
    if not valid_transactions:
        logger.warning("No valid transactions found after pre-validation")
        return BulkTransactionResponse(
            success_count=0,
            failure_count=len(transactions),
            total_processed=len(transactions),
            inserted_ids=[],
            errors=pre_validation_errors
        )
    
    # Perform bulk insert
    inserted_ids, db_errors = transactions_repo.bulk_insert_transactions(valid_transactions)
    
    # Combine all errors
    all_errors = pre_validation_errors + db_errors
    
    success_count = len(inserted_ids)
    failure_count = len(transactions) - success_count
    
    logger.info(f"Bulk transaction insert completed: {success_count} successful, {failure_count} failed")
    
    return BulkTransactionResponse(
        success_count=success_count,
        failure_count=failure_count,
        total_processed=len(transactions),
        inserted_ids=inserted_ids,
        errors=all_errors if all_errors else None
    )
