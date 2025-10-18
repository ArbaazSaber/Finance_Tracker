from typing import Annotated
from pydantic import BaseModel, StringConstraints

class Tag(BaseModel):
    tag_id: int
    tag_name: Annotated[str, StringConstraints(min_length=1)]
    category_id: int


class TagBase(BaseModel):
    tag_name: Annotated[str, StringConstraints(min_length=1)]
    category_name: Annotated[str, StringConstraints(min_length=1)]