from typing import Optional, List, Dict

from utils.logger import logger
from models.account import AccountBase, AccountUpdate

from services.banks_service import fetch_bank_id_by_name, fetch_bank_name_by_id
from services.users_service import get_user_by_username, get_user_by_id

import repositories.accounts_repository as account_repo 


def fetch_account_by_id(acc_id: int) -> Optional[Dict]:
    """
    Retrieve the Accounts using the Account ID.

    Args:
        acc_id (int): ID of the account.

    Returns:
        Optional[AccountBase]: Account Details if found, otherwise None.
    """
    account = account_repo.get_account_by_id(acc_id)
    if not account:
        logger.warning(f"No Account found with ID: {acc_id}")
        return None

    return account

def fetch_accounts_by_user(user_id: int) -> Optional[List[Dict]]:
    """
    Fetch all accounts for a given user.

    Returns:
        List[tuple]: A list of tuples, each containing account details.
    """
    accounts = account_repo.get_accounts_by_user(user_id)
    if not accounts:
        logger.info(f"No accounts found for user {user_id}")
        return None
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
    if bank_id is None:
        raise ValueError("Bank Not Found")

    user = get_user_by_username(account.user_name)
    if not user or not user.get("user_id"):
        raise ValueError("User Not Found")
    user_id = user["user_id"]

    acc_id = account_repo.create_account(account.acc_name.strip(), user_id, bank_id)
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

    # Determine new name and bank id
    new_acc_name = acc_data.acc_name.strip() if acc_data.acc_name else existing.get('acc_name')
    if not new_acc_name:
        logger.warning("Account Name cannot be empty")
        return False

    if acc_data.bank_name:
        new_bank_id = fetch_bank_id_by_name(acc_data.bank_name)
        if new_bank_id is None:
            logger.warning(f"Bank {acc_data.bank_name} does not exist")
            return False
    else:
        new_bank_id = existing.get('bank_id')

    updated = account_repo.update_account(acc_id=acc_id, acc_name=new_acc_name, bank_id=new_bank_id)
    if updated:
        logger.info(f"Updated account {acc_id} to Account Name='{new_acc_name}', BankId={new_bank_id}")
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
