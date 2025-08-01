from typing import Optional, List

from utils.logger import logger
from models.account import AccountBase, AccountUpdate

from services.banks_service import fetch_bank_id_by_name
from services.users_service import get_user_by_username

import repositories.accounts_repository as account_repo 

def fetch_account_by_id(acc_id: int) -> Optional[AccountBase]:
    """
    Retrieve the Accounts using the Account ID.

    Args:
        acc_id (int): ID of the account.

    Returns:
        Optional[AccountBase]: Account Details if found, otherwise None.
    """
    bank = account_repo.get_account_by_id(acc_id)
    if not bank:
        logger.warning(f"No Account found with ID: {acc_id}")
        return None

    return bank

def fetch_accounts_by_user(user_id: int) -> Optional[List[AccountBase]]:
    """
    Fetch all accounts for a given user.

    Returns:
        List[tuple]: A list of tuples, each containing account details.
    """
    accounts = account_repo.get_accounts_by_user(user_id)
    logger.info(f"Fetched {len(accounts)} Accounts")
    return accounts
    
def create_account(account: AccountBase) -> Optional[int]:
    """
    Insert a new bank after ensuring it does not already exist.

    Args:
        bank_name (str): Name of the bank to insert.

    Returns:
        int: The ID of the newly inserted bank.

    Raises:
        ValueError: If the bank name is empty or already exists.
    """
    bank_id = fetch_bank_id_by_name(account.bank_name)
    if not bank_id:
        raise ValueError("Bank Not Found")

    user_id = get_user_by_username(account.user_name)
    if not user_id:
        raise ValueError("User Not Found")
    
    acc_id = account_repo.create_account(account.acc_name, user_id, bank_id)
    logger.info(f"Inserted new account: {account.acc_name} with ID: {acc_id}")
    return acc_id

def update_account(acc_id: int, acc_data: AccountUpdate) -> bool:
    """
    Update an existing tagging rule.

    Args:
        rule_id (int): ID of the rule to update.
        keyword (AccountUpdate): Account Details to Update

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    existing = account_repo.get_account_by_id(acc_id)
    if not existing:
        logger.warning(f"Cannot update: Account with ID {acc_id} does not exist")
        return False

    # Default to existing values if not provided
    if not acc_data.bank_name:
        new_bank_id = fetch_bank_id_by_name(existing['bank_name'])

    new_acc_name = acc_data.acc_name.strip() if acc_data.acc_name else existing['acc_name']
    new_bank_id = fetch_bank_id_by_name(acc_data.bank_name) 

    if not new_acc_name:
        logger.warning("Account Name cannot be empty")
        return False

    if new_bank_id is None:
        logger.warning(f"Bank {acc_data.bank_name} does not exist")
        return False

    updated = account_repo.update_account(acc_id=acc_id, acc_name=new_acc_name, bank_id=new_bank_id)
    if updated:
        logger.info(f"Updated tagging account {acc_id} to Account Name='{new_acc_name}', Bank={acc_data.bank_name}")
    else:
        logger.error(f"Failed to update Account with ID {acc_id}")
    return updated


def deactivate_account(acc_id: int) -> bool:
    """
    Marks the account as inactive.

    Args:
        acc_id (int): The account's ID.

    Returns:
        bool: True if deactivated, False otherwise.
    """
    return account_repo.deactivate_account(acc_id)
