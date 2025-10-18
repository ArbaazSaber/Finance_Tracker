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
    """
    Insert transactions using bulk API endpoint for better performance.
    """
    if not transactions:
        print("No transactions to insert")
        return
    
    try:
        # Use bulk endpoint for better performance
        # Convert transactions to dictionaries with proper datetime serialization
        serialized_transactions = []
        for tx in transactions:
            tx_dict = tx.dict()
            # Convert datetime to ISO format string
            if tx_dict.get('transaction_time'):
                tx_dict['transaction_time'] = tx_dict['transaction_time'].isoformat()
            # Convert Decimal to float for JSON serialization
            if tx_dict.get('amount'):
                tx_dict['amount'] = float(tx_dict['amount'])
            serialized_transactions.append(tx_dict)
        
        payload = {"transactions": serialized_transactions}
        res = requests.post(f"{API_BASE}/transactions/bulk", json=payload)
        res.raise_for_status()
        
        result = res.json()
        print(f"Bulk insert completed: {result['success_count']} successful, {result['failure_count']} failed")
        
        if result.get('errors'):
            print("Errors during insert:")
            for error in result['errors']:
                print(f"  - {error}")
        
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error inserting transactions: {str(e)}")
        raise
