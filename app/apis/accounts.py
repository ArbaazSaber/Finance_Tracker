from fastapi import APIRouter, HTTPException
from typing import List, Optional

import services.accounts_service as accounts_service
from models.account import AccountBase, AccountUpdate

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("/{acc_id}")
def get_account_by_acc_id(acc_id: int):
    account = accounts_service.fetch_account_by_id(acc_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.get("/user/{user_id}")
def get_accounts_for_user(user_id: int):
    accounts = accounts_service.fetch_accounts_by_user(user_id)
    if not accounts:
        raise HTTPException(status_code=404, detail="Accounts not found")
    return accounts

@router.post("/", status_code=201)
def create_account(account: AccountBase):
    created = accounts_service.create_account(account)
    if not created:
        raise HTTPException(status_code=400, detail="Failed to create Account")
    return created

# FIX THIS
@router.put("/{acc_id}")
def update_account(acc_id: int, update_data: AccountUpdate):
    updated = accounts_service.update_account(
        acc_id,
        acc_data=update_data,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Failed to update Account")
    return accounts_service.fetch_account_by_id(acc_id)

@router.delete("/{acc_id}", status_code=204)
def delete_account(acc_id: int):
    deleted = accounts_service.deactivate_account(acc_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tagging account not found")