from db.database import get_connection
from utils.logger import logger
from psycopg2.extras import RealDictCursor, execute_values
import psycopg2

from typing import Optional, List, Tuple
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
        row = cursor.fetchone()
        return Transaction(**row) if row else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_transaction_by_id: {e}")
        return None
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
        INSERT INTO transactions(transaction_time, description, old_description, amount, reference_id, type, tag_id, acc_id, user_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING transaction_id
    """
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (
            transaction.transaction_time,
            transaction.description,
            transaction.old_description,
            transaction.amount,
            transaction.reference_id,
            transaction.type.value if transaction.type else None,
            transaction.tag_id,
            transaction.acc_id,
            transaction.user_id,
        ))
        transaction_id = cursor.fetchone()[0]
        conn.commit()
        return transaction_id
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

def bulk_insert_transactions(transactions: List[Transaction]) -> Tuple[List[int], List[str]]:
    """
    Bulk inserts multiple transactions and returns a tuple of (inserted_ids, errors).
    Uses execute_values for efficient bulk operations with ON CONFLICT support.
    Skips duplicate transactions based on (reference_id, acc_id) unique constraint.
    """
    if not transactions:
        return [], []
    
    conn = None
    cursor = None
    inserted_ids = []
    errors = []
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Prepare the data for bulk insert
        transaction_data = []
        for i, transaction in enumerate(transactions):
            try:
                # Validate required fields
                if not transaction.user_id or not transaction.acc_id:
                    errors.append(f"Transaction {i}: Missing required user_id or acc_id")
                    continue
                    
                transaction_data.append((
                    transaction.transaction_time,
                    transaction.description,
                    transaction.old_description,
                    transaction.amount,
                    transaction.reference_id,
                    transaction.type.value if transaction.type else None,
                    transaction.tag_id,
                    transaction.acc_id,
                    transaction.user_id,
                ))
            except Exception as e:
                errors.append(f"Transaction {i}: Data validation error - {str(e)}")
        
        if not transaction_data:
            return [], errors
        
        # Execute bulk insert using execute_values which properly supports ON CONFLICT
        query = """
            INSERT INTO transactions(transaction_time, description, old_description, amount, reference_id, type, tag_id, acc_id, user_id) 
            VALUES %s
            ON CONFLICT ON CONSTRAINT unique_reference_per_account DO NOTHING
        """
        
        execute_values(
            cursor,
            query,
            transaction_data,
            page_size=1000
        )
        
        conn.commit()
        logger.info(f"Successfully processed {len(transaction_data)} transactions (duplicates automatically skipped)")
        
        # Return empty list for inserted_ids
        inserted_ids = []
        
    except psycopg2.Error as e:
        logger.error(f"[Repository] Database error in bulk_insert_transactions: {e}")
        if conn:
            conn.rollback()
        errors.append(f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"[Repository] Unexpected error in bulk_insert_transactions: {e}")
        if conn:
            conn.rollback()
        errors.append(f"Unexpected error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return inserted_ids, errors
