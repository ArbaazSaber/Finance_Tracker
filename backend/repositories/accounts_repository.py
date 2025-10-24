from psycopg2.extras import RealDictCursor
from typing import Optional, List, Dict

from db.database import get_connection
from utils.logger import logger
from models.account import Account

def get_account_by_id(acc_id: int) -> Optional[Dict]:
    """Fetch the account by id and return a dict with account and related names."""
    query = (
        "SELECT a.acc_id, a.acc_name, a.user_id, a.bank_id, a.is_active, a.balance, a.currency, "
        "u.username AS user_name, b.bank_name "
        "FROM users u JOIN accounts a ON a.user_id = u.user_id JOIN banks b ON a.bank_id = b.bank_id "
        "WHERE a.acc_id = %s AND a.is_active = true"
    )
    conn = None
    cursor = None
    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (acc_id,))
        result = cursor.fetchone()
        return dict(result) if result else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_account_by_id: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_accounts_by_user(user_id: int) -> Optional[List[Dict]]:
    """Fetch all active accounts for a given user id and return list of dicts."""
    query = (
        "SELECT a.acc_id, a.acc_name, a.user_id, a.bank_id, a.is_active, a.balance, a.currency, "
        "u.username AS user_name, b.bank_name "
        "FROM users u JOIN accounts a ON a.user_id = u.user_id JOIN banks b ON a.bank_id = b.bank_id "
        "WHERE u.user_id = %s AND a.is_active = true"
    )
    conn = None
    cursor = None
    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        return [dict(r) for r in rows] if rows else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_accounts_by_user: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_account(acc_name: str, user_id: int, bank_id: int, balance: int = 0, currency: str = "USD") -> Optional[int]:
    """Insert a new account and return the generated acc_id."""
    query = "INSERT INTO accounts (acc_name, user_id, bank_id, is_active, balance, currency) VALUES (%s, %s, %s, true, %s, %s) RETURNING acc_id"
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (acc_name, user_id, bank_id, balance, currency))
        acc_id = cursor.fetchone()[0]
        conn.commit()
        return acc_id
    except Exception as e:
        logger.error(f"[Repository] Error in create_account: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_account(acc_id: int, acc_name: str, bank_id: int, balance: Optional[int] = None, currency: Optional[str] = None) -> bool:
    """
    Updates the Account Details for an account given a account ID.
    Returns if the update was successful.
    """
    # Build dynamic query based on which fields are provided
    update_fields = ["acc_name = %s", "bank_id = %s"]
    params = [acc_name, bank_id]
    
    if balance is not None:
        update_fields.append("balance = %s")
        params.append(balance)
    
    if currency is not None:
        update_fields.append("currency = %s")
        params.append(currency)
    
    params.append(acc_id)
    query = f"UPDATE accounts SET {', '.join(update_fields)} WHERE acc_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"[Repository] Error in update_account: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def deactivate_account(acc_id: int) -> bool:
    """
    Soft Deletes the account from the database.
    Returns if the delete was successful.
    """
    query = "UPDATE accounts SET is_active = false WHERE acc_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (acc_id,))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"[Repository] Error in deactivate_account: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()