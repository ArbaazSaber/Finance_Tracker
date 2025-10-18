from pydantic import BaseModel

class TagBase(BaseModel):
    tag_name: str
    category_name: str