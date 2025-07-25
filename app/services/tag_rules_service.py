from typing import List, Optional, Dict

from models.tag_rule import TagRuleBase
from utils.logger import logger
from utils.util_functions import format_string
from services.tag_service import fetch_tag_id_by_name

import repositories.tag_rules_repository as tag_rules_repo

def fetch_all_tagging_rules() -> List[Dict]:
    """
    Fetch all tagging rules with associated tag and keyword info.

    Returns:
        List[Dict]: A list of rules with rule_id, keyword, tag_id, and tag_name.
    """
    rules = tag_rules_repo.get_all_tagging_rules()
    logger.info(f"Fetched {len(rules)} tagging rules")
    return rules

def fetch_rules_for_tag(tag_name: str) -> List[Dict]:
    """
    Fetch all tagging rules for a specific tag.

    Args:
        tag_id (int): The ID of the tag.

    Returns:
        List[Dict]: A list of rules for that tag.
    """
    tag_id = fetch_tag_id_by_name(tag_name)
    if not tag_id:
        logger.warning(f"Tag {tag_name} does not exist")
        return []

    rules = tag_rules_repo.get_tagging_rules_for_tag(tag_id)
    logger.info(f"Fetched {len(rules)} rules for tag {tag_name}")
    return rules

def fetch_rule_by_id(rule_id: int) -> Optional[Dict]:
    """
    Fetch a specific tagging rule by its ID.

    Args:
        rule_id (int): The ID of the rule.

    Returns:
        Optional[Dict]: Rule details or None if not found.
    """
    rule = tag_rules_repo.get_tagging_rule_by_id(rule_id)
    if rule:
        logger.info(f"Found tagging rule with ID {rule_id}")
    else:
        logger.warning(f"No tagging rule found with ID {rule_id}")
    return rule

def create_tagging_rule(tag_rule: TagRuleBase) -> Optional[int]:
    """
    Create a new tagging rule with a keyword and tag.

    Args:
        keyword (str): The keyword to match.
        tag_name (str): The tag to assign if matched.

    Returns:
        Optional[int]: The ID of the newly created rule, or None if failed.
    """
    keyword = tag_rule.keyword.strip().lower()
    if not keyword:
        logger.warning("Keyword must not be empty")
        return None

    tag_id = fetch_tag_id_by_name(format_string(tag_rule.tag_name))
    if not tag_id:
        logger.warning(f"Tag {tag_rule.tag_name} does not exist")
        return None

    rule_id = tag_rules_repo.insert_tagging_rule(keyword, tag_id)
    if rule_id:
        logger.info(f"Created tagging rule {rule_id} for keyword '{keyword}' and tag_id {tag_id}")
    else:
        logger.error("Failed to create tagging rule")
    return rule_id

def update_tagging_rule(rule_id: int, tag_rule: TagRuleBase) -> bool:
    """
    Update an existing tagging rule.

    Args:
        rule_id (int): ID of the rule to update.
        keyword (Optional[str]): New keyword (if updating).
        tag_id (Optional[int]): New tag_id (if updating).

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    existing = tag_rules_repo.get_tagging_rule_by_id(rule_id)
    if not existing:
        logger.warning(f"Cannot update: Rule with ID {rule_id} does not exist")
        return False

    # Default to existing values if not provided
    tag_id = fetch_tag_id_by_name(format_string(tag_rule.tag_name))

    new_keyword = tag_rule.keyword.strip().lower() if tag_rule.keyword else existing['keyword']
    new_tag_id = tag_id if tag_id is not None else existing['tag_id']

    if not new_keyword:
        logger.warning("Keyword cannot be empty")
        return False

    if tag_id is not None:
        logger.warning(f"Tag {tag_rule.tag_name} does not exist")
        return False

    updated = tag_rules_repo.update_tagging_rule(rule_id, new_keyword, new_tag_id)
    if updated:
        logger.info(f"Updated tagging rule {rule_id} to keyword='{new_keyword}', tag_id={new_tag_id}")
    else:
        logger.error(f"Failed to update tagging rule with ID {rule_id}")
    return updated


def delete_tagging_rule(rule_id: int) -> bool:
    """
    Delete a tagging rule by its ID.

    Args:
        rule_id (int): The ID of the rule to delete.

    Returns:
        bool: True if deleted, False otherwise.
    """
    existing = tag_rules_repo.get_tagging_rule_by_id(rule_id)
    if not existing:
        logger.warning(f"Cannot delete: Rule with ID {rule_id} does not exist")
        return False

    success = tag_rules_repo.delete_tagging_rule(rule_id)
    if success:
        logger.info(f"Deleted tagging rule with ID {rule_id}")
    else:
        logger.error(f"Failed to delete tagging rule with ID {rule_id}")
    return success
