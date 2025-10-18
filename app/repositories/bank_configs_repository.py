from db.database import get_connection
from utils.logger import logger
from models.bank_config import BankColumnMapping

from typing import Optional, List, Dict

def get_bank_rule_by_id(bank_id: int) -> Optional[Dict]:
    """
    Fetches the bank rule given a bank id.
    Returns None if the bank rule does not exist.
    """
    query = "SELECT * FROM bank_rules WHERE bank_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (bank_id,))
        desc = [col[0] for col in cursor.description]
        result = cursor.fetchone()
        if result:
            return dict(zip(desc, result))
        return None
    except Exception as e:
        logger.error(f"[Repository] Error in get_bank_rule_by_id: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_bank_columns_by_rule_id(bank_rule_id: int) -> List[BankColumnMapping]:
    """
    Fetches the columns to use for a bank given a bank rule id.
    Returns an empty list if the columns do not exist.
    """
    query = "SELECT column_mapping_id, bank_rule_id, original_column, mapped_column FROM bank_column_mappings WHERE bank_rule_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (bank_rule_id,))
        desc = [col[0] for col in cursor.description]
        results = cursor.fetchall()
        return [BankColumnMapping(**dict(zip(desc, row))) for row in results]
    except Exception as e:
        logger.error(f"[Repository] Error in get_bank_columns_by_rule_id: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()