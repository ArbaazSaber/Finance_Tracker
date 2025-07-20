from typing import List, Optional

from utils.logger import logger
import repositories.category_repository as category_repo

def fetch_all_categories() -> List[tuple]:
    """
    Fetch all Categories with their IDs and names.

    Returns:
        List[tuple]: A list of tuples, each containing category_id and category_name.
    """
    Categories = category_repo.get_all_categories()
    logger.info(f"Fetched {len(Categories)} Categories")
    return Categories


def fetch_all_category_names() -> List[str]:
    """
    Fetch the names of all Categories.

    Returns:
        List[str]: A list of category names.
    """
    names = category_repo.get_all_category_names()
    logger.info(f"Fetched category names: {names}")
    return names


def fetch_category_id_by_name(category_name: str) -> Optional[int]:
    """
    Retrieve the category ID using the category name.

    Args:
        category_name (str): Name of the category.

    Returns:
        Optional[int]: Category ID if found, otherwise None.
    """
    if not category_name.strip():
        raise ValueError("Category name must not be empty")

    category = category_repo.get_category_id(category_name.strip())
    if not category:
        logger.warning(f"No category found with name: {category_name}")
        return None

    return category


def fetch_category_name_by_id(category_id: int) -> Optional[str]:
    """
    Retrieve the category name using the category ID.

    Args:
        category_id (int): ID of the category.

    Returns:
        Optional[str]: Category name if found, otherwise None.
    """
    category = category_repo.get_category_name(category_id)
    if not category:
        logger.warning(f"No category found with ID: {category_id}")
        return None
    return category


def add_new_category(category_name: str) -> int:
    """
    Insert a new category after ensuring it does not already exist.

    Args:
        category_name (str): Name of the category to insert.

    Returns:
        int: The ID of the newly inserted category.

    Raises:
        ValueError: If the category name is empty or already exists.
    """
    category_name = category_name.strip()
    if not category_name:
        raise ValueError("Category name must not be empty")

    existing_category = category_repo.get_category_id(category_name)
    if existing_category:
        raise ValueError(f"Category '{category_name}' already exists with ID {existing_category[0]}")

    category_id = category_repo.insert_category(category_name)
    logger.info(f"Inserted new category: {category_name} with ID: {category_id}")
    return category_id


def fetch_total_category_count() -> int:
    """
    Get the total number of Categories in the database.

    Returns:
        int: Total count of Categories.
    """
    count = category_repo.count_categories()
    logger.info(f"Total category count: {count}")
    return count


def fetch_latest_category_name() -> Optional[str]:
    """
    Get the name of the most recently added category.

    Returns:
        Optional[str]: Category name if available, otherwise None.
    """
    latest = category_repo.get_latest_category_entry()
    logger.info(f"Latest category: {latest}")
    return latest