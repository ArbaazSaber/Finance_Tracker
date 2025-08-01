from fastapi import APIRouter, HTTPException, status

import services.banks_service as banks_service
from models.bank import BankCreate

router = APIRouter(prefix="/banks", tags=["Banks"])


@router.get("/", summary="Get all banks")
def get_all_banks():
    return banks_service.fetch_all_banks()


@router.get("/names", summary="Get all bank names")
def get_all_bank_names():
    return banks_service.fetch_all_bank_names()


@router.get("/count", summary="Get total number of banks")
def get_bank_count():
    return {"count": banks_service.fetch_total_bank_count()}


@router.get("/latest", summary="Get the latest inserted bank name")
def get_latest():
    latest = banks_service.fetch_latest_bank_name()
    if latest is None:
        raise HTTPException(status_code=404, detail="No banks found")
    return {"latest_bank": latest}


@router.get("/without-rules", summary="Get banks without associated rules")
def get_banks_without_rules_api():
    return banks_service.fetch_banks_without_rules()


@router.get("/name/{bank_id}", summary="Get bank name by ID")
def get_bank_name(bank_id: int):
    try:
        return {"bank_name": banks_service.fetch_bank_name_by_id(bank_id)}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))


@router.get("/id/{bank_name}", summary="Get bank ID by name")
def get_bank_id(bank_name: str):
    try:
        return {"bank_id": banks_service.fetch_bank_id_by_name(bank_name)}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))


@router.post("/", summary="Insert a new bank")
def insert_new_bank(data: BankCreate):
    try:
        bank_id = banks_service.add_new_bank(data)
        return {"bank_id": bank_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insertion failed: {str(e)}")