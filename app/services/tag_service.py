from typing import List, Optional

from utils.logger import logger
from models.tag import TagBase
import repositories.tag_repository as tag_repo
import repositories.category_repository as category_repository


def fetch_all_tags() -> List[tuple]:
    """
    Fetch all Tags with their IDs and names.

    Returns:
        List[tuple]: A list of tuples, each containing tag_id and tag_name.
    """
    tags = tag_repo.get_all_tags()
    logger.info(f"Fetched {len(tags)} Tags")
    return tags


def fetch_all_tag_names() -> List[str]:
    """
    Fetch the names of all Tags.

    Returns:
        List[str]: A list of tag names.
    """
    names = tag_repo.get_all_tag_names()
    logger.info(f"Fetched tag names: {names}")
    return names


def fetch_tag_id_by_name(tag_name: str) -> Optional[int]:
    """
    Retrieve the tag ID using the tag name.

    Args:
        tag_name (str): Name of the tag.

    Returns:
        Optional[int]: Tag ID if found, otherwise None.
    """
    if not tag_name.strip():
        raise ValueError("Tag name must not be empty")

    tag = tag_repo.get_tag_id(tag_name.strip())
    if not tag:
        logger.warning(f"No tag found with name: {tag_name}")
        return None

    return tag


def fetch_tag_name_by_id(tag_id: int) -> Optional[str]:
    """
    Retrieve the tag name using the tag ID.

    Args:
        tag_id (int): ID of the tag.

    Returns:
        Optional[str]: Tag name if found, otherwise None.
    """
    tag = tag_repo.get_tag_name(tag_id)
    if not tag:
        logger.warning(f"No tag found with ID: {tag_id}")
        return None
    return tag


def upsert_tag(tag: TagBase) -> int:
    """
    Upsert a new tag. Update the category it does not already exist.

    Args:
        tag (TagBase): Name of the tag and the category to insert.

    Returns:
        int: The ID of the tag.

    Raises:
        ValueError: If the tag name is empty.
    """
    tag_name = tag.tag_name.strip()
    category_name = tag.category_name.strip()
    if not tag_name:
        raise ValueError("Tag name must not be empty")
    if not category_name:
        raise ValueError("Category name must not be empty")

    category_id = category_repository.get_category_id(category_name)
    if not category_id:
        raise ValueError(f"No Category Found with the name: {tag.category_name}")
    
    existing_tag = tag_repo.get_tag_id(tag_name)
    if existing_tag:
        logger.info("Tag already present! Updating the category...")
        tag_id = tag_repo.update_tag(tag_name, category_id)
    else:
        logger.info("Inserting the tag...")
        tag_id = tag_repo.insert_tag(tag_name, category_id)

    return tag_id


def fetch_total_tag_count() -> int:
    """
    Get the total number of Tags in the database.

    Returns:
        int: Total count of Tags.
    """
    count = tag_repo.count_tags()
    logger.info(f"Total tag count: {count}")
    return count


def fetch_latest_tag_name() -> Optional[str]:
    """
    Get the name of the most recently added tag.

    Returns:
        Optional[str]: Tag name if available, otherwise None.
    """
    latest = tag_repo.get_latest_tag_entry()
    logger.info(f"Latest tag: {latest}")
    return latest

def fetch_category_name_of_tag(tag_name: str) -> Optional[str]:
    """
    Get the category name of the tag.

    Args:
        tag_name (str): Name of the tag.

    Returns:
        Optional[str]: Category name if found, otherwise None.
    """
    category = tag_repo.get_category_of_tag(tag_name)
    if not category:
        logger.warning(f"No category found with Name: {tag_name}")
        return None
    return category