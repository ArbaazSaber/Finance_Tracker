from fastapi import APIRouter, HTTPException

import services.bank_configs_service as bank_configs_service

router = APIRouter(prefix="/bank-configs", tags=["Bank Configs"])

@router.get("/{bank_name}", summary="Get bank config by bank name")
def get_bank_config(bank_name: str):
    try:
        return bank_configs_service.fetch_bank_config(bank_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
