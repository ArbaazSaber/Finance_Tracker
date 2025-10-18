from fastapi import APIRouter, HTTPException, status

import services.categories_service as categories_service
from models.category import CategoryCreate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", summary="Get all categories")
def get_all_categories():
    return categories_service.fetch_all_categories()


@router.get("/names", summary="Get all category names")
def get_all_category_names():
    return categories_service.fetch_all_category_names()


@router.get("/count", summary="Get total number of categories")
def get_category_count():
    return {"count": categories_service.fetch_total_category_count()}


@router.get("/latest", summary="Get the latest inserted category name")
def get_latest():
    latest = categories_service.fetch_latest_category_name()
    if latest is None:
        raise HTTPException(status_code=404, detail="No categories found")
    return {"latest_category": latest}


@router.get("/name/{category_id}", summary="Get category name by ID")
def get_category_name(category_id: int):
    try:
        return {"category_name": categories_service.fetch_category_name_by_id(category_id)}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))


@router.get("/id/{category_name}", summary="Get category ID by name")
def get_category_id(category_name: str):
    try:
        return {"category_id": categories_service.fetch_category_id_by_name(category_name)}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))


@router.post("/", summary="Insert a new category")
def insert_new_category(data: CategoryCreate):
    try:
        category_id = categories_service.add_new_category(data)
        return {"category_id": category_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insertion failed: {str(e)}")