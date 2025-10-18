from typing import Annotated
from pydantic import BaseModel, StringConstraints


class Category(BaseModel):
    category_id: int
    category_name: Annotated[str, StringConstraints(min_length=1)]


class CategoryCreate(BaseModel):
    category_name: Annotated[str, StringConstraints(min_length=1)]