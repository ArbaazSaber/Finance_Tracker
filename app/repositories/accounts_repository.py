from psycopg2.extras import RealDictCursor
from typing import Optional, List

from db.database import get_connection
from utils.logger import logger
from models.account import AccountBase

def get_account_by_id(acc_id: int) -> Optional[AccountBase]:
    """
    Fetches the Account given a Account ID.
    Returns None if the Account does not exist.
    """
    query = "SELECT a.acc_name, u.username, b.bank_name FROM users u JOIN accounts a ON a.user_id = u.user_id JOIN banks b ON a.bank_id = b.bank_id WHERE a.acc_id = %s AND a.is_active = true"
    conn = None
    cursor = None

    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (acc_id,))
        result = cursor.fetchone()
        return result if result else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_user_by_id: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
def get_accounts_by_user(user_id: int) -> Optional[List[AccountBase]]:
    """
    Fetches the Accounts given a User ID.
    Returns None if the Accounts do not exist.
    """
    query = "SELECT a.acc_name, u.username, b.bank_name FROM users u JOIN accounts a ON a.user_id = u.user_id JOIN banks b ON a.bank_id = b.bank_id WHERE u.user_id = %s AND a.is_active = true"
    conn = None
    cursor = None

    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        return result if result else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_user_by_id: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_account(acc_name: str, user_id: int, bank_id: int) -> Optional[int]:
    """
    Inserts a user into the database.
    Returns the inserted user_id or None on failure.
    """
    query = "INSERT INTO accounts (acc_name, bank_id, user_id, is_active) VALUES (%s, %s, %s, true) RETURNING acc_id"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (acc_name, bank_id, user_id))
        user_id = cursor.fetchone()[0]
        conn.commit()
        return user_id
    except Exception as e:
        logger.error(f"[Repository] Error in insert_user: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_account(acc_id: int, acc_name: str, bank_id: int) -> bool:
    """
    Updates the Account Details for an account given a account ID.
    Returns if the update was successful.
    """
    query = "UPDATE accounts SET acc_name = %s, bank_id = %s WHERE acc_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (acc_name, bank_id, acc_id))
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
        logger.error(f"[Repository] Error in deactivate_user: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()