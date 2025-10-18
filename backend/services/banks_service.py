from typing import List, Optional

from utils.logger import logger
from models.bank import BankCreate

import repositories.banks_repository as bank_repo

def fetch_all_banks() -> List[tuple]:
    """
    Fetch all banks with their IDs and names.

    Returns:
        List[tuple]: A list of tuples, each containing bank_id and bank_name.
    """
    banks = bank_repo.get_all_banks()
    logger.info(f"Fetched {len(banks)} banks")
    return banks


def fetch_all_bank_names() -> List[str]:
    """
    Fetch the names of all banks.

    Returns:
        List[str]: A list of bank names.
    """
    names = bank_repo.get_all_bank_names()
    logger.info(f"Fetched bank names: {names}")
    return names


def fetch_bank_id_by_name(bank_name: str) -> Optional[int]:
    """
    Retrieve the bank ID using the bank name.

    Args:
        bank_name (str): Name of the bank.

    Returns:
        Optional[int]: Bank ID if found, otherwise None.
    """
    if not bank_name.strip():
        raise ValueError("Bank name must not be empty")

    bank = bank_repo.get_bank_id(bank_name.strip())
    if not bank:
        logger.warning(f"No bank found with name: {bank_name}")
        return None

    return bank


def fetch_bank_name_by_id(bank_id: int) -> Optional[str]:
    """
    Retrieve the bank name using the bank ID.

    Args:
        bank_id (int): ID of the bank.

    Returns:
        Optional[str]: Bank name if found, otherwise None.
    """
    bank = bank_repo.get_bank_name(bank_id)
    if not bank:
        logger.warning(f"No bank found with ID: {bank_id}")
        return None
    return bank


def add_new_bank(bank: BankCreate) -> int:
    """
    Insert a new bank after ensuring it does not already exist.

    Args:
        bank_name (str): Name of the bank to insert.

    Returns:
        int: The ID of the newly inserted bank.

    Raises:
        ValueError: If the bank name is empty or already exists.
    """
    bank_name = bank.bank_name.strip()
    if not bank_name:
        raise ValueError("Bank name must not be empty")

    existing_bank = bank_repo.get_bank_id(bank_name)
    if existing_bank:
        raise ValueError(f"Bank '{bank_name}' already exists with ID {existing_bank[0]}")

    bank_id = bank_repo.insert_bank(bank_name)
    logger.info(f"Inserted new bank: {bank_name} with ID: {bank_id}")
    return bank_id


def fetch_total_bank_count() -> int:
    """
    Get the total number of banks in the database.

    Returns:
        int: Total count of banks.
    """
    count = bank_repo.count_banks()
    logger.info(f"Total bank count: {count}")
    return count


def fetch_latest_bank_name() -> Optional[str]:
    """
    Get the name of the most recently added bank.

    Returns:
        Optional[str]: Bank name if available, otherwise None.
    """
    latest = bank_repo.get_latest_bank_entry()
    logger.info(f"Latest bank: {latest}")
    return latest


def fetch_banks_without_rules() -> List[str]:
    """
    Get the names of banks that do not have any rules defined.

    Returns:
        List[str]: A list of bank names without associated rules.
    """
    banks = bank_repo.get_banks_without_rules()
    logger.info(f"Banks without rules: {banks}")
    return banks