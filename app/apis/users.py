from fastapi import APIRouter, HTTPException

import services.user_service as user_service
from models.user import UserCreate

router = APIRouter(prefix="/users", users=["Users"])

@router.get("/", summary="Get all users")
def get_all_users():
    return user_service.fetch_all_users()

@router.post("/", summary="Upsert a new user")
def upsert_user(data: TagBase):
    try:
        user_id = user_service.upsert_user(data)
        return {"user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insertion failed: {str(e)}")