from typing import Annotated
from pydantic import BaseModel, StringConstraints

class TaggingRule(BaseModel):
    rule_id: int
    keyword: Annotated[str, StringConstraints(min_length=1)]
    tag_id: int


class TagRuleBase(BaseModel):
    keyword: Annotated[str, StringConstraints(min_length=1)]
    tag_name: Annotated[str, StringConstraints(min_length=1)]