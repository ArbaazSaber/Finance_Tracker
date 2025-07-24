from db.database import get_connection
from utils.logger import logger
from psycopg2.extras import RealDictCursor

from typing import Optional, List, Dict

def get_all_tagging_rules() -> Optional[List[Dict]]:
    """
    Returns a list of all (rule_id, keyword, tag_id) tuples.
    """
    query = "SELECT tr.rule_id, tr.keyword, t.tag_name FROM tagging_rules tr JOIN tags t ON tr.tag_id = t.tag_id ORDER BY rule_id"
    conn = None
    cursor = None

    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"[Repository] Error in get_all_tagging_rules: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_tagging_rule_by_id(rule_id: int) -> Optional[Dict]:
    """
    Returns a tagging rule by its ID.
    """
    query = "SELECT tr.rule_id, tr.keyword, t.tag_name FROM tagging_rules tr JOIN tags t ON tr.tag_id = t.tag_id WHERE rule_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (rule_id,))
        return cursor.fetchone()
    except Exception as e:
        logger.error(f"[Repository] Error in get_tagging_rule_by_id: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_tagging_rules_for_tag(tag_id: int) -> Optional[Dict]:
    """
    Returns all tagging rules for a tag.
    """
    query = "SELECT rule_id, keyword, tag_id FROM tagging_rules WHERE tag_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (tag_id,))
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"[Repository] Error in get_tagging_rules_for_tag: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_tagging_rule(keyword: str, tag_id: int) -> Optional[int]:
    """
    Inserts a new tagging rule and returns the generated rule_id.
    """
    query = """
        INSERT INTO tagging_rules (keyword, tag_id)
        VALUES (%s, %s)
        RETURNING rule_id
    """
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (keyword, tag_id))
        rule_id = cursor.fetchone()[0]
        conn.commit()
        return rule_id
    except Exception as e:
        logger.error(f"[Repository] Error in insert_tagging_rule: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_tagging_rule(rule_id: int) -> bool:
    """
    Deletes a tagging rule by its ID. Returns True if successful.
    """
    query = "UPDATE tagging_rules SET is_active = false WHERE rule_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (rule_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"[Repository] Error in delete_tagging_rule: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_tagging_rule(rule_id: int, keyword: str, tag_id: int) -> bool:
    """
    Updates an existing tagging rule. Returns True if update is successful.
    """
    query = """
        UPDATE tagging_rules
        SET keyword = %s, tag_id = %s
        WHERE rule_id = %s
    """
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (keyword, tag_id, rule_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"[Repository] Error in update_tagging_rule: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
