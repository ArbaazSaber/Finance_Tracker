from typing import Optional, Dict
import re

from utils.logger import logger
from utils.security import hash_password, verify_password
from models.user import UserCreate, UserAuth
import repositories.users_repository as users_repository

def get_user_by_id(user_id: int) -> Optional[Dict]:
    """
    Fetches a user by their ID.

    Args:
        user_id (int): The user's unique ID.

    Returns:
        Optional[Dict]: User data if found, else None.
    """
    if user_id <= 0:
        logger.warning(f"Invalid user_id: {user_id}")
        return None

    return users_repository.get_user_by_id(user_id)


def get_user_by_username(username: str) -> Optional[Dict]:
    """
    Fetches a user by their username.

    Args:
        username (str): The username to search.

    Returns:
        Optional[Dict]: User data if found, else None.
    """
    if not username.strip():
        logger.warning("Empty username provided.")
        return None

    return users_repository.get_user_by_username(username.strip())


def get_user_by_email(email: str) -> Optional[Dict]:
    """
    Fetches a user by their email address.

    Args:
        email (str): The email address to search.

    Returns:
        Optional[Dict]: User data if found, else None.
    """
    if not is_valid_email(email):
        logger.warning(f"Invalid email format: {email}")
        return None

    return users_repository.get_user_by_email(email.lower())


def create_user(user_data: UserCreate) -> Optional[int]:
    """
    Creates a new user in the system.

    Args:
        user_data (UserCreate): User data from request.

    Returns:
        Optional[int]: The newly created user's ID or None if creation failed.
    """
    if not user_data.username.strip():
        logger.warning("Username is empty.")
        return None
    if not is_valid_email(user_data.email):
        logger.warning("Invalid email format.")
        return None

    hashed_pwd = hash_password(user_data.password)
    return users_repository.insert_user(
        username=user_data.username.strip(),
        email=user_data.email.lower(),
        hashed_password=hashed_pwd
    )


def update_last_login(user_id: int) -> bool:
    """
    Updates the last_login field of the user to current time.

    Args:
        user_id (int): The user's unique ID.

    Returns:
        bool: True if updated, False otherwise.
    """
    return users_repository.update_last_login(user_id)


def update_email(user_id: int, email: str) -> bool:
    """
    Updates the email address of a user.

    Args:
        user_id (int): The user's ID.
        email (str): New email address.

    Returns:
        bool: True if updated, False otherwise.
    """
    if not is_valid_email(email):
        logger.warning(f"Invalid email: {email}")
        return False

    return users_repository.update_email(user_id, email.lower())


def update_password(user_id: int, password: str) -> bool:
    """
    Updates the hashed password for a user.

    Args:
        user_id (int): The user's ID.
        password (str): New plain password.

    Returns:
        bool: True if updated, False otherwise.
    """
    if not password.strip():
        logger.warning("Password is empty.")
        return False

    hashed_pwd = hash_password(password)
    return users_repository.update_password(user_id, hashed_pwd)


def deactivate_user(user_id: int) -> bool:
    """
    Marks the user as inactive.

    Args:
        user_id (int): The user's ID.

    Returns:
        bool: True if deactivated, False otherwise.
    """
    return users_repository.deactivate_user(user_id)

def is_valid_email(email: str) -> bool:
    """
    Simple email format validator.

    Args:
        email (str): Email string.

    Returns:
        bool: True if valid, else False.
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email or "") is not None

def authenticate_user(user_auth: UserAuth) -> Optional[int]:
    """
    Authenticates a user by verifying the provided credentials.

    Args:
        username_or_email (str): Username or email used to log in.
        password (str): Plaintext password to verify.

    Returns:
        Optional[int]: User ID if authentication is successful, else None.
    """
    if not user_auth.username_or_email.strip() or not user_auth.password:
        logger.warning("Authentication Failed: Missing Credentials")
        return None
    
    user_auth.username_or_email = user_auth.username_or_email.strip()

    # Try by email first, then fallback to username
    user = users_repository.get_user_by_username(user_auth.username_or_email)
    if user is None:
        user = users_repository.get_user_by_email(user_auth.username_or_email.strip())

    if user is None:
        logger.info(f"Authentication failed: User '{user_auth.username_or_email}' not found.")
        return None

    if not user["is_active"]:
        logger.info(f"Authentication failed: User '{user_auth.username_or_email}' is inactive.")
        return None

    if not verify_password(user["password_hash"], user_auth.password):
        logger.info(f"Authentication failed: Incorrect password for user '{user_auth.username_or_email}'.")
        return None
    
    return user.get("user_id", None) 