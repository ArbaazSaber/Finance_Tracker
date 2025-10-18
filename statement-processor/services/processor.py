import pandas as pd
# import yaml
from utils.helper import fetch_bank_config, get_tagging_rules

class DataHandling:
    def __init__(self, bank:str, statement_path:str):
        self.bank = bank
        self.statement_path = statement_path
        self.bank_config = fetch_bank_config(self.bank)
        self.tagging_rules = get_tagging_rules()

    def load_excel_statement(self) -> pd.DataFrame:
        if self.bank_config is None:
            return "Bank not Present"
        df = pd.read_excel(
            self.statement_path,
            skiprows = self.bank_config["skiprows"],
            skipfooter = self.bank_config["skipfooter"],
            usecols = self.bank_config["usecols"],
            engine = self.bank_config["engine"]
        )
        print(type(df))
        return df

    def clean_description(self, desc: str) -> str:
        reason = desc
        if desc.startswith('UPI'):
            reason = desc.split('-')[-1]
        if 'UPI' not in reason and not "PAY" in reason: return reason
        return desc

    def clean_statement(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.bank_config is None:
            return "Bank not Present"
        df = df.rename(columns=self.bank_config["column_mapping"])
        df = df.dropna(how="all")
        df["description"] = df["description"].str.strip().str.upper().apply(self.clean_description)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        df = df.dropna(subset=["date"])

        df["withdrawal"] = pd.to_numeric(df["withdrawal"], errors="coerce").fillna(0)
        df["deposit"] = pd.to_numeric(df["deposit"], errors="coerce").fillna(0)

        df["amount"] = df["deposit"] - df["withdrawal"]
        df["type"] = df["amount"].apply(lambda x: "Credit" if x > 0 else "Debit")
        df = df.drop(columns=["withdrawal", "deposit"])
        df["bank"] = self.bank
        return df

    # FIX THIS FUNCTION
    def get_tag(self, desc: str):
        tagging_rules = get_tagging_rules()
        if desc in tagging_rules:
            return tagging_rules[desc][0]
        return "Unknown"

    def apply_tags(self, df:pd.DataFrame) -> pd.DataFrame:
        df["tag"] = df["description"].apply(self.get_tag)
        return df