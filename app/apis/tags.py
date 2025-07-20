from db.database import get_connection
import utils.util_functions as utils
import apis.categories as categories
from utils.logger import logger

from typing import Optional

def get_tag_id(tag_name: str) -> Optional[int]:
    tag_name = utils.format_string(tag_name)

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT tag_id FROM tags WHERE tag_name=%s", (tag_name,))

        result = cursor.fetchone()
        if not result:
            raise ValueError("Tag Does Not Exist")

        tag_id = result[0]

        logger.info(f"Tag - {tag_name} with ID - {tag_id}")
        return tag_id
    except Exception as e:
        logger.error(e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_tag_name(tag_id: int) -> Optional[str]:
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT tag_name FROM tags WHERE tag_id=%s", (tag_id,))

        result = cursor.fetchone()
        if not result:
            raise ValueError("Tag Does Not Exist")

        tag_name = result[0]

        logger.info(f"Tag - {tag_name} with ID - {tag_id}")
        return tag_name
    except Exception as e:
        logger.error(e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_tags() -> Optional[list]:
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT t.tag_id, t.tag_name, c.category_name FROM tags t JOIN categories c ON t.category_id = c.category_id")

        tags = cursor.fetchall()
        if not tags:
            raise ValueError("Tag Table Empty")

        logger.info(f"Tags - {tags}")
        return tags
    except Exception as e:
        logger.error(e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_tag_ids():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT tag_id FROM tags")

        result = cursor.fetchall()
        if not result:
            raise ValueError("Tag Table Empty")

        tag_ids = [tag[0] for tag in result]

        logger.info(f"Tag IDs - {tag_ids}")
        return tag_ids
    except Exception as e:
        logger.error(e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_tag_names():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT tag_name FROM tags")

        result = cursor.fetchall()
        if not result:
            raise ValueError("Tag Table Empty")

        tag_names = [tag[0] for tag in result]

        logger.info(f"Tag IDs - {tag_names}")
        return tag_names
    except Exception as e:
        logger.error(e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_tag(tag_name: str, category_name: str):
    tag_name = utils.format_string(tag_name)
    category_name = utils.format_string(category_name)

    try:
        conn = get_connection()
        cursor = conn.cursor()

        category_id = categories.get_category_id(category_name)
        if not category_id:
            return ValueError("Category Does Not Exist")

        cursor.execute("INSERT INTO tags (tag_name, category_id) VALUES (%s,%s) RETURNING tag_id;", (tag_name, category_id))

        tag_id = cursor.fetchone()[0]
        conn.commit()

        logger.info(f"Inserted tag: {tag_name} with ID: {tag_id}")
    except Exception as e:
        logger.exception(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def count_tags() -> int:
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM tags")
        result = cursor.fetchone()
        if not result:
            return 0
        return result[0]
    except Exception as e:
        logger.exception(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def get_latest_tag_entry() -> str:
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT tag_name FROM tags ORDER BY tag_id DESC LIMIT 1")
        result = cursor.fetchone()
        if not result:
            return None
        return result[0]
    except Exception as e:
        logger.exception(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
        
def get_category_of_tag(tag_name: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT tag_name FROM tags ORDER BY tag_id DESC LIMIT 1")
        result = cursor.fetchone()
        if not result:
            return None
        return result[0]
    except Exception as e:
        logger.exception(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()