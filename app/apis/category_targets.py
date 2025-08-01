from fastapi import APIRouter, HTTPException
from typing import Optional, List

from models.category_target import CategoryTarget
import services.category_targets_service as category_targets_service

router = APIRouter(prefix="/category-targets", tags=["Category Targets"])

@router.post("/", response_model=Optional[int])
async def create_category_target(category_target: CategoryTarget):
    target_id = category_targets_service.add_category_target(category_target)
    if target_id is None:
        raise HTTPException(status_code=500, detail="Failed to create category target.")
    return target_id

@router.get("/user/{user_id}", response_model=List[CategoryTarget])
async def read_all_targets_by_user(user_id: int):
    return category_targets_service.fetch_all_targets_by_user(user_id)


@router.get("/user/{user_id}/current", response_model=List[CategoryTarget])
async def read_current_targets_by_user(user_id: int):
    return category_targets_service.fetch_current_targets_by_user(user_id)


@router.get("/{category_id}/user/{user_id}", response_model=List[CategoryTarget])
async def read_target_by_category_user(category_id: int, user_id: int):
    result = category_targets_service.fetch_target_by_category_user(category_id, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Target not found.")
    return result