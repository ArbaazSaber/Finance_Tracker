from typing import List, Optional

from utils.logger import logger
from models.category_target import CategoryTarget

import repositories.category_targets_repository as category_target_repo


def add_category_target(category_target: CategoryTarget) -> Optional[int]:
    """
    Add a new category target to the database.

    Args:
        category_target (CategoryTarget): The category target data to insert.

    Returns:
        Optional[int]: The newly created target ID if successful, otherwise None.
    """
    try:
        return category_target_repo.insert_category_target(category_target)
    except Exception as e:
        logger.info(f"Error adding category target: {e}")
        return None


def fetch_all_targets_by_user(user_id: int) -> List[CategoryTarget]:
    """
    Retrieve all category targets for a specific user.

    Args:
        user_id (int): ID of the user whose targets are to be fetched.

    Returns:
        List[CategoryTarget]: A list of category targets for the user.
    """
    try:
        return category_target_repo.get_all_targets_by_user(user_id)
    except Exception as e:
        logger.info(f"Error fetching all targets for user {user_id}: {e}")
        return []


def fetch_current_targets_by_user(user_id: int) -> List[CategoryTarget]:
    """
    Retrieve the latest (current) target for each category associated with a user.

    Args:
        user_id (int): ID of the user whose current targets are to be fetched.

    Returns:
        List[CategoryTarget]: A list of the most recent category targets per category.
    """
    try:
        return category_target_repo.get_current_targets_by_user(user_id)
    except Exception as e:
        logger.info(f"Error fetching current targets for user {user_id}: {e}")
        return []

def fetch_target_by_category_user(category_id: int, user_id: int) -> List[CategoryTarget]:
    """
    Retrieve the most recent target for a specific category and user.

    Args:
        category_id (int): ID of the category.
        user_id (int): ID of the user.

    Returns:
        Optional[CategoryTarget]: The most recent category target if found, otherwise None.
    """
    try:
        return category_target_repo.get_target_by_category_user(category_id, user_id)
    except Exception as e:
        logger.info(f"Error fetching target for category {category_id} and user {user_id}: {e}")
        return None
