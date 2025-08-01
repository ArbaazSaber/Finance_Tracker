from db.database import get_connection
from utils.logger import logger
from psycopg2.extras import RealDictCursor

from typing import Optional, List, Dict
from models.transaction import Transaction

def get_transaction_by_id(transaction_id: int) -> Optional[Transaction]:
    """
    Returns a Transaction from an ID.
    """
    query = "SELECT * FROM transactions WHERE transaction_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (transaction_id,))
        return Transaction(**cursor.fetchone())
    except Exception as e:
        logger.error(f"[Repository] Error in get_transaction_by_id: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_transaction_for_user(user_id: int) -> List[Transaction]:
    """
    Returns the Transactions for a user.
    """
    query = "SELECT * FROM transactions WHERE user_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        return [Transaction(**row) for row in results]
    except Exception as e:
        logger.error(f"[Repository] Error in get_all_transaction_for_user: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_transaction_for_account(acc_id: int) -> List[Transaction]:
    """
    Returns the Transactions for a user.
    """
    query = "SELECT * FROM transactions WHERE acc_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (acc_id,))
        results = cursor.fetchall()
        return [Transaction(**row) for row in results]
    except Exception as e:
        logger.error(f"[Repository] Error in get_all_transaction_for_account: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_transaction(transaction: Transaction) -> Optional[int]:
    """
    Inserts a new transaction and returns the generated transaction_id.
    """
    query = """
        INSERT INTO transactions(transaction_time, description, old_description, amount, reference_id, type, tag_id, category_id, acc_id, user_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING transaction_id
    """
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (transaction.transaction_time,
            transaction.description,
            transaction.old_description,
            transaction.amount,
            transaction.reference_id,
            transaction.type,
            transaction.tag_id,
            transaction.category_id,
            transaction.acc_id,
            transaction.user_id
        ))
        rule_id = cursor.fetchone()[0]
        conn.commit()
        return rule_id
    except Exception as e:
        logger.error(f"[Repository] Error in insert_transaction: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_transaction(transaction_id: int, transaction: Transaction) -> bool:
    """
    Updates an existing transaction. Returns True if successful, False otherwise.
    """
    query = """
        UPDATE transactions
        SET
            description = %s,
            tag_id = %s,
            category_id = %s,
            acc_id = %s,
            user_id = %s,
            modified_at = CURRENT_TIMESTAMP
        WHERE transaction_id = %s
    """
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (
            transaction.description,
            transaction.tag_id,
            transaction.category_id,
            transaction.acc_id,
            transaction.user_id,
            transaction_id
        ))
        conn.commit()
        return cursor.rowcount > 0  # True if a row was updated
    except Exception as e:
        logger.error(f"[Repository] update_transaction failed: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()