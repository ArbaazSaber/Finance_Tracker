from fastapi import APIRouter, HTTPException, status

import services.tags_service as tags_service
from models.tag import TagBase

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("/", summary="Get all tags")
def get_all_tags():
    return tags_service.fetch_all_tags()

@router.get("/count", summary="Get total number of tags")
def get_tag_count():
    return {"count": tags_service.fetch_total_tag_count()}


@router.get("/latest", summary="Get the latest inserted tag name")
def get_latest():
    latest = tags_service.fetch_latest_tag_name()
    if latest is None:
        raise HTTPException(status_code=404, detail="No tags found")
    return {"latest_tag": latest}


@router.get("/name/{tag_name}", summary="Get tag by name")
def get_tag_by_name(tag_name: str):
    try:
        return tags_service.fetch_tag_by_name(tag_name)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))

@router.get("/id/{tag_id}", summary="Get tag by ID")
def get_tag_by_id(tag_id: str):
    try:
        return tags_service.fetch_tag_by_id(tag_id)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))

@router.post("/", summary="Upsert a new tag")
def upsert_tag(data: TagBase):
    try:
        tag_id = tags_service.upsert_tag(data)
        return {"tag_id": tag_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insertion failed: {str(e)}")