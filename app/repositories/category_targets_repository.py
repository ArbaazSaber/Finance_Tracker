from typing import List, Optional
from db.database import get_connection

from psycopg2.extras import RealDictCursor
from typing import List, Optional, Dict
from utils.logger import logger

def insert_category_target(percentage: float, category_id: int, user_id: int) -> Optional[int]:
    """
    Inserts a new category target for a user.

    Args:
        percentage (float): Target percentage (0–100).
        category_id (int): Foreign key to category.
        user_id (int): Foreign key to user.

    Returns:
        Optional[int]: ID of the newly created target, or None on failure.
    """
    query = """
    INSERT INTO category_targets (percentage, category_id, user_id)
    VALUES (%s, %s, %s)
    RETURNING target_id
    """
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (percentage, category_id, user_id))
        target_id = cursor.fetchone()[0]
        conn.commit()
        return target_id
    except Exception as e:
        logger.error(f"[Repository] insert_category_target failed: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_all_targets_by_user(user_id: int) -> List[Dict]:
    """
    Returns all category targets for a given user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[Tuple]: List of tuples containing target info.
    """
    query = """
    SELECT target_id, percentage, start_date, category_id
    FROM category_targets
    WHERE user_id = %s
    ORDER BY start_date DESC
    """
    conn = None
    cursor = None
    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"[Repository] get_targets_by_user failed: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_current_targets_by_user(user_id: int) -> List[Dict]:
    """
    Returns the current category targets for a given user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[Tuple]: List of tuples containing target info.
    """
    query = """
        SELECT DISTINCT ON (category_id, user_id) target_id, percentage, start_date, category_id, user_id
        FROM category_targets
        WHERE user_id = %s
        ORDER BY category_id, user_id, start_date DESC
    """
    conn = None
    cursor = None
    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"[Repository] get_targets_by_user failed: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_target_percentage(target_id: int, percentage: float) -> bool:
    """
    Updates the percentage of a specific category target.

    Args:
        target_id (int): The target ID to update.
        percentage (float): New percentage value.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    query = """
    UPDATE category_targets
    SET percentage = %s
    WHERE target_id = %s
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (percentage, target_id))
        conn.commit()
        return cursor.rowcount == 1
    except Exception as e:
        logger.error(f"[Repository] update_target_percentage failed: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_target(target_id: int) -> bool:
    """
    Deletes a category target by ID.

    Args:
        target_id (int): The target ID to delete.

    Returns:
        bool: True if deleted, False otherwise.
    """
    query = "DELETE FROM category_targets WHERE target_id = %s"
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (target_id,))
        conn.commit()
        return cursor.rowcount == 1
    except Exception as e:
        logger.error(f"[Repository] delete_target failed: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_target_by_category_user(category_id: int, user_id: int) -> Optional[Dict]:
    """
    Fetches a category target by (category_id, user_id) pair.

    Args:
        category_id (int): The category ID.
        user_id (int): The user ID.

    Returns:
        Optional[Tuple]: Target row or None if not found.
    """
    query = """
    SELECT target_id, percentage, start_date
    FROM category_targets
    WHERE category_id = %s AND user_id = %s
    """
    conn = None
    cursor = None
    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (category_id, user_id))
        return cursor.fetchone()
    except Exception as e:
        logger.error(f"[Repository] get_target_by_category_user failed: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
