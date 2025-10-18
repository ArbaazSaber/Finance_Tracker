from db.database import get_connection
from utils.logger import logger

from psycopg2.extras import RealDictCursor
from typing import Optional, List, Tuple

def get_tag_by_name(tag_name: str) -> Optional[int]:
    """
    Fetches the tag ID given a tag name.
    Returns None if the tag does not exist.
    """
    query = "SELECT c.category_id, c.category_name, t.tag_name, t.tag_id FROM categories c JOIN tags t ON t.category_id = c.category_id WHERE t.tag_name = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (tag_name.strip(),))
        return cursor.fetchone() if cursor.rowcount > 0 else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_tag_id: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_tag_by_id(tag_id: int) -> Optional[str]:
    """
    Fetches the tag name given a tag ID.
    Returns None if the tag is not found.
    """
    query = "SELECT c.category_id, c.category_name, t.tag_name, t.tag_id FROM categories c JOIN tags t ON t.category_id = c.category_id WHERE t.tag_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (tag_id,))
        return cursor.fetchone() if cursor.rowcount > 0 else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_tag_name: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_tags() -> List[Tuple[int, str]]:
    """
    Returns a list of all (tag_id, tag_name) tuples.
    """
    query = "SELECT t.tag_id, t.tag_name, c.category_id, c.category_name FROM tags t JOIN categories c ON c.category_id = t.category_id ORDER BY tag_name"
    conn = None
    cursor = None

    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"[Repository] Error in get_all_tags: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_tag(tag_name: str, category_id: int) -> Optional[int]:
    """
    Inserts a tag into the database.
    Returns the inserted tag_id or None on failure.
    """
    query = "INSERT INTO tags (tag_name, category_id) VALUES (%s,%s) RETURNING tag_id;"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (tag_name.strip(),category_id))
        tag_id = cursor.fetchone()[0]
        conn.commit()
        return tag_id
    except Exception as e:
        logger.error(f"[Repository] Error in insert_tag: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_tag(tag_name: str, category_id: int) -> Optional[int]:
    """
    Updates a tag into the database.
    Returns the inserted tag_id or None on failure.
    """
    query = "UPDATE tags SET category_id = %s WHERE tag_name = %s RETURNING tag_id;"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (category_id,tag_name.strip()))
        tag_id = cursor.fetchone()[0]
        conn.commit()
        return tag_id
    except Exception as e:
        logger.error(f"[Repository] Error in update_tag: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def count_tags() -> int:
    """
    Count the total number of tags in the database.

    Returns:
        int: Total number of tags.

    Raises:
        Exception: If a database error occurs.
    """
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM tags;")
        result = cursor.fetchone()

        return result[0] if result else 0

    except Exception as e:
        logger.exception("Failed to count tags")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_latest_tag_entry() -> Optional[str]:
    """
    Fetches the most recently inserted tag name.
    """
    query = "SELECT tag_name FROM tags ORDER BY tag_id DESC LIMIT 1"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_latest_tag_entry: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_category_of_tag(tag_name: str) -> Optional[str]:
    """
    Fetches the category ID of a given tag.
    Returns None if the tag is not found.
    """
    query = "SELECT c.category_name FROM tags t JOIN categories c ON t.category_id = c.category_id WHERE t.tag_name = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query,(tag_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_category_of_tag: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()