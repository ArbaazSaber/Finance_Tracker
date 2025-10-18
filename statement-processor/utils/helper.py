import requests
from typing import Optional, Dict, List

def fetch_bank_config(bank: str) -> Optional[Dict]:
    """
    Fetch bank configuration from API.
    """
    try:
        response = requests.get(f"http://127.0.0.1:8000/bank-configs/{bank}", 
                              verify=False, timeout=10)
        
        if response.status_code == 200:
            bank_config = response.json()
            # Convert column mapping to dictionary format
            if bank_config and "column_mapping" in bank_config:
                col_rename_map = {
                    col["original_column"]: col["mapped_column"] 
                    for col in bank_config["column_mapping"]
                }
                bank_config["column_mapping"] = col_rename_map
            return bank_config
        else:
            print(f"Bank config not found for {bank}: HTTP {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bank config for {bank}: {str(e)}")
        return None

def get_tagging_rules() -> List[Dict]:
    """
    Fetch tagging rules from API.
    """
    try:
        response = requests.get("http://127.0.0.1:8000/tagging_rules/", 
                              verify=False, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch tagging rules: HTTP {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tagging rules: {str(e)}")
        return []

# Remove the print loop that runs on import
# for item in get_tagging_rules():
#     print(item)
