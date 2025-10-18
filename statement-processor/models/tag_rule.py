from pydantic import BaseModel

class TagRuleBase(BaseModel):
    keyword: str
    tag_name: str

class TaggingRuleOut(BaseModel):
    rule_id: int
    keyword: str
    tag_name: str
