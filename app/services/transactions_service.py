from typing import List, Optional

from utils.logger import logger
from models.transaction import Transaction, TransactionUpsert

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

def add_transaction(transaction: Transaction) -> Optional[int]:
    if not transaction.user_id or not transaction.acc_id:
        logger.warning("Transaction must include user_id and acc_id")
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
        category_id=new_data.category_id or existing.category_id,
        acc_id=new_data.acc_id or existing.acc_id,
        user_id=new_data.user_id or existing.user_id
    )

    return transactions_repo.update_transaction(transaction_id, updated)
