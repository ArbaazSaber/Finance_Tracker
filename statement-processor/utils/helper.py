import requests

def fetch_bank_config(bank: str):
    response = requests.get(f"http://127.0.0.1:8000/bank-configs/{bank}", verify=False)
    bank_config = response.json() if response.status_code == 200 else None
    col_rename_map = {col["original_column"]: col["mapped_column"] for col in bank_config["column_mapping"]} if bank_config else {}
    if bank_config:
        bank_config["column_mapping"] = col_rename_map
    return bank_config

def get_tagging_rules() -> dict:
    tagging_rules_response = requests.get(f"http://127.0.0.1:8000/tagging_rules", verify=False)
    return tagging_rules_response.json()
    # rules = {}
    # for _, row in tagging_rules.iterrows():
    #     rules[row["description"].strip().upper()] = (row["tag"].strip().upper(), row["category"].strip().upper())
    # return rules

for item in get_tagging_rules():
    print(item)