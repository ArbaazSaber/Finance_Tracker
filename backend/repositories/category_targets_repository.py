from typing import List, Optional
from psycopg2.extras import RealDictCursor

from db.database import get_connection
from utils.logger import logger
from models.category_target import CategoryTarget

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


def get_all_targets_by_user(user_id: int) -> List[CategoryTarget]:
    """
    Returns all category targets for a given user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[Tuple]: List of tuples containing target info.
    """
    query = """
    SELECT *
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
        results = cursor.fetchall()
        return [CategoryTarget(**row) for row in results]
    except Exception as e:
        logger.error(f"[Repository] get_targets_by_user failed: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_current_targets_by_user(user_id: int) -> List[CategoryTarget]:
    """
    Returns the current category targets for a given user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[Tuple]: List of tuples containing target info.
    """
    query = """
        SELECT DISTINCT ON (category_id, user_id) *
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
        results = cursor.fetchall()
        return [CategoryTarget(**row) for row in results]
    except Exception as e:
        logger.error(f"[Repository] get_targets_by_user failed: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_target_by_category_user(category_id: int, user_id: int) -> List[CategoryTarget]:
    """
    Fetches a category target by (category_id, user_id) pair.

    Args:
        category_id (int): The category ID.
        user_id (int): The user ID.

    Returns:
        Optional[Tuple]: Target row or None if not found.
    """
    query = """
    SELECT *
    FROM category_targets
    WHERE category_id = %s AND user_id = %s
    ORDER BY start_date DESC
    """
    conn = None
    cursor = None
    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (category_id, user_id))
        results = cursor.fetchall()
        return [CategoryTarget(**row) for row in results]
    except Exception as e:
        logger.error(f"[Repository] get_target_by_category_user failed: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
