from fastapi import APIRouter, HTTPException

import services.user_service as user_service
from models.user import UserAuth, UserCreate, UserPasswordUpdateRequest

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/id/{user_id}", summary="Get user by ID")
def get_user_by_id(user_id: int):
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/username/{username}", summary="Get user by username")
def get_user_by_username(username: str):
    user = user_service.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/email/{email}", summary="Get user by email")
def get_user_by_email(email: str):
    user = user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", summary="Create a new user")
def create_user(user_data: UserCreate):
    user_id = user_service.create_user(user_data)
    if user_id is None:
        raise HTTPException(status_code=400, detail="User creation failed")
    return {"user_id": user_id}

@router.get("/authenticate", summary="Authenticate user")
def authenticate_user(user_auth: UserAuth):
    user = user_service.authenticate_user(user_auth)
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return user

@router.put("/password/{user_id}", summary="Update user password")
def update_password(user_id: int, new_password: UserPasswordUpdateRequest):
    success = user_service.update_password(user_id, new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Password update failed")
    return {"message": "Password updated successfully"}

@router.put("/last-login/{user_id}", summary="Update last login time")
def update_last_login(user_id: int):
    success = user_service.update_last_login(user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Last login update failed")
    return {"message": "Last login updated successfully"}

@router.put("/email/{user_id}", summary="Update user email")
def update_email(user_id: int, new_email: str):
    success = user_service.update_email(user_id, new_email)
    if not success:
        raise HTTPException(status_code=400, detail="Email update failed")
    return {"message": "Email updated successfully"}

@router.delete("/{user_id}", summary="Delete user by ID")
def delete_user(user_id: int):
    success = user_service.deactivate_user(user_id)
    if not success:
        raise HTTPException(status_code=400, detail="User deletion failed")
    return {"message": "User deleted successfully"}