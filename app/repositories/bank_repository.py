from db.database import get_connection
from utils.logger import logger

from typing import Optional, List, Tuple

def get_bank_id(bank_name: str) -> Optional[int]:
    """
    Fetches the bank ID given a bank name.
    Returns None if the bank does not exist.
    """
    query = "SELECT bank_id FROM banks WHERE bank_name = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (bank_name.strip(),))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_bank_id: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_bank_name(bank_id: int) -> Optional[str]:
    """
    Fetches the bank name given a bank ID.
    Returns None if the bank is not found.
    """
    query = "SELECT bank_name FROM banks WHERE bank_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (bank_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_bank_name: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_banks() -> List[Tuple[int, str]]:
    """
    Returns a list of all (bank_id, bank_name) tuples.
    """
    query = "SELECT bank_id, bank_name FROM banks ORDER BY bank_name"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"[Repository] Error in get_all_banks: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_bank_names() -> List[str]:
    """
    Returns a list of all bank names sorted alphabetically.
    """
    query = "SELECT bank_name FROM banks ORDER BY bank_name"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"[Repository] Error in get_all_bank_names: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_bank(bank_name: str) -> Optional[int]:
    """
    Inserts a bank into the database.
    Returns the inserted bank_id or None on failure.
    """
    query = "INSERT INTO banks (bank_name) VALUES (%s) RETURNING bank_id"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (bank_name.strip(),))
        bank_id = cursor.fetchone()[0]
        conn.commit()
        return bank_id
    except Exception as e:
        logger.error(f"[Repository] Error in insert_bank: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def count_banks() -> int:
    """
    Count the total number of banks in the database.

    Returns:
        int: Total number of banks.

    Raises:
        Exception: If a database error occurs.
    """
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM banks;")
        result = cursor.fetchone()

        return result[0] if result else 0

    except Exception as e:
        logger.exception("Failed to count banks")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_latest_bank_entry() -> Optional[str]:
    """
    Fetches the most recently inserted bank name.
    """
    query = "SELECT bank_name FROM banks ORDER BY bank_id DESC LIMIT 1"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_latest_bank_entry: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_banks_without_rules() -> List[str]:
    """
    Returns bank names that do not have any rule entries in bank_rules table.
    """
    query = """
        SELECT b.bank_name 
        FROM banks b 
        WHERE NOT EXISTS (
            SELECT 1 FROM bank_rules br WHERE br.bank_id = b.bank_id
        ) 
        ORDER BY b.bank_name
    """
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"[Repository] Error in get_banks_without_rules: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
