from typing import List, Optional

from utils.logger import logger
from models.bank_config import BankRule

import repositories.banks_repository as bank_repo
import repositories.bank_configs_repository as bank_config_repo

def fetch_bank_config(bank_name: str) -> Optional[BankRule]:
    """
    Fetch the bank rule for their IDs and names.

    Returns:
        List[tuple]: A list of tuples, each containing bank_id and bank_name.
    """
    bank_id = bank_repo.get_bank_id(bank_name=bank_name)
    if not bank_id:
        raise ValueError("Bank does not exist!")
    bank_rule_dict = bank_config_repo.get_bank_rule_by_id(bank_id)
    if not bank_rule_dict:
        raise ValueError("Bank Rule does not exist for this bank!")
    bank_columns = bank_config_repo.get_bank_columns_by_rule_id(bank_rule_dict["bank_rule_id"])
    if not bank_columns:
        raise ValueError("Bank Columns do not exist for this bank!")
    
    bank_rule = BankRule(
        bank_rule_id = bank_rule_dict["bank_rule_id"],
        bank_id = bank_rule_dict["bank_id"],
        skiprows = bank_rule_dict["skiprows"],
        skipfooter = bank_rule_dict["skipfooter"],
        usecols = bank_rule_dict["usecols"],
        engine = bank_rule_dict["engine"],
        column_mapping=bank_columns
        )
    
    return bank_rule
