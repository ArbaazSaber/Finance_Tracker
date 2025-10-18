from fastapi import APIRouter, HTTPException
from typing import List, Optional

import services.tag_rules_service as tag_rules_service
from models.tag_rule import TagRuleBase

router = APIRouter(prefix="/tagging_rules", tags=["Tagging Rules"])

@router.get("/")
def get_all_rules():
    rules = tag_rules_service.fetch_all_tagging_rules()
    return rules

@router.get("/{rule_id}")
def get_rule_by_id(rule_id: int):
    rule = tag_rules_service.fetch_rule_by_id(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Tagging rule not found")
    return rule

@router.get("/tag/{tag_name}")
def get_rules_for_tag(tag_name: str):
    rules = tag_rules_service.fetch_rules_for_tag(tag_name)
    if not rules:
        raise HTTPException(status_code=404, detail="Tagging rules not found")
    return rules

@router.post("/", status_code=201)
def create_rule(rule: TagRuleBase):
    created = tag_rules_service.create_tagging_rule(rule)
    if not created:
        raise HTTPException(status_code=400, detail="Failed to create tagging rule")
    return created

# FIX THIS
@router.put("/{rule_id}")
def update_rule(rule_id: int, update_data: TagRuleBase):
    updated = tag_rules_service.update_tagging_rule(
        rule_id,
        tag_rule=update_data,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Failed to update tagging rule")
    return tag_rules_service.fetch_rule_by_id(rule_id)

@router.delete("/{rule_id}", status_code=204)
def delete_rule(rule_id: int):
    deleted = tag_rules_service.delete_tagging_rule(rule_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tagging rule not found")
