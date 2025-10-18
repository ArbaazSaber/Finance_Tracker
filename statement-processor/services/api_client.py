import requests
from typing import List
from models.bank_config import BankRule
from models.transaction import Transaction

API_BASE = "http://127.0.0.1:8000"

def get_bank_config(bank_name: str) -> BankRule:
    res = requests.get(f"{API_BASE}/banks/config/{bank_name}")
    res.raise_for_status()
    return BankRule(**res.json())

def insert_transactions(transactions: List[Transaction]):
    for tx in transactions:
        res = requests.post(f"{API_BASE}/transactions", json=tx.dict())
        res.raise_for_status()
