from db.database import get_connection
from utils.logger import logger
from psycopg2.extras import RealDictCursor

from typing import Optional, Dict

def get_user_by_id(user_id: int) -> Optional[Dict]:
    """
    Fetches the User given a User ID.
    Returns None if the User does not exist.
    """
    query = "SELECT * FROM users WHERE user_id = %s AND is_active = true"
    conn = None
    cursor = None

    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result if result else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_user_by_id: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_user_by_username(username: str) -> Optional[Dict]:
    """
    Fetches the User given a Username.
    Returns None if the User does not exist.
    """
    query = "SELECT * FROM users WHERE username = %s AND is_active = true"
    conn = None
    cursor = None

    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result if result else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_user_by_username: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_user_by_email(email: str) -> Optional[Dict]:
    """
    Fetches the User given an email.
    Returns None if the User does not exist.
    """
    query = "SELECT * FROM users WHERE email = %s AND is_active = true"
    conn = None
    cursor = None

    try:
        conn = get_connection(RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result if result else None
    except Exception as e:
        logger.error(f"[Repository] Error in get_user_by_email: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_user(username: str, email: str, hashed_password: str) -> Optional[int]:
    """
    Inserts a user into the database.
    Returns the inserted user_id or None on failure.
    """
    query = "INSERT INTO users (username, email, password_hash, is_active) VALUES (%s, %s, %s, %s) RETURNING user_id"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (username, email, hashed_password, True))
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

def update_last_login(user_id: int) -> bool:
    """
    Updates the last login time into the database.
    Returns if the user_id on successfully updating.
    """
    query = "UPDATE users SET last_login = NOW() WHERE user_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"[Repository] Error in update_last_login: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_email(user_id: int, email: str) -> bool:
    """
    Updates the email for a userid into the database.
    Returns if the user_id on successfully updating.
    """
    query = "UPDATE users SET email = %s WHERE user_id = %s "
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (email, user_id))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"[Repository] Error in update_last_login: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_password(user_id: int, hashed_password: str) -> bool:
    """
    Updates the Password for a user given a user ID.
    Returns if the update was successful.
    """
    query = "UPDATE users SET password_hash = %s WHERE user_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (hashed_password, user_id))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"[Repository] Error in update_password: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def deactivate_user(user_id: int) -> bool:
    """
    Soft Deletes the user from the database.
    Returns if the delete was successful.
    """
    query = "UPDATE users SET is_active = false WHERE user_id = %s"
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
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