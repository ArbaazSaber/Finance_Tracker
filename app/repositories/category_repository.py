from db.database import get_connection
from utils.logger import logger

from typing import Optional, List, Tuple

def get_category_id(category_name: str) -> Optional[int]:
    """
    Fetches the category ID given a category name.
    Returns None if the category does not exist.
    """
    query = "SELECT category_id FROM categories WHERE category_name = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (category_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_category_id: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_category_name(category_id: int) -> Optional[str]:
    """
    Fetches the category name given a category ID.
    Returns None if the category is not found.
    """
    query = "SELECT category_name FROM categories WHERE category_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (category_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_category_name: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_categories() -> List[Tuple[int, str]]:
    """
    Returns a list of all (category_id, category_name) tuples.
    """
    query = "SELECT category_id, category_name FROM categories ORDER BY category_name"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"[Repository] Error in get_all_categories: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_category_names() -> List[str]:
    """
    Returns a list of all category names sorted alphabetically.
    """
    query = "SELECT category_name FROM categories ORDER BY category_name"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"[Repository] Error in get_all_category_names: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_category(category_name: str) -> Optional[int]:
    """
    Inserts a category into the database.
    Returns the inserted category_id or None on failure.
    """
    query = "INSERT INTO categories (category_name) VALUES (%s) RETURNING category_id"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (category_name,))
        category_id = cursor.fetchone()[0]
        conn.commit()
        return category_id
    except Exception as e:
        logger.error(f"[Repository] Error in insert_category: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def count_categories() -> int:
    """
    Count the total number of categories in the database.

    Returns:
        int: Total number of categories.

    Raises:
        Exception: If a database error occurs.
    """
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM categories;")
        result = cursor.fetchone()

        return result[0] if result else 0

    except Exception as e:
        logger.exception("Failed to count categories")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_latest_category_entry() -> Optional[str]:
    """
    Fetches the most recently inserted category name.
    """
    query = "SELECT category_name FROM categories ORDER BY category_id DESC LIMIT 1"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_latest_category_entry: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()