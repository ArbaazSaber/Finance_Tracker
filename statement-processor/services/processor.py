import pandas as pd
from typing import List
from datetime import datetime
from decimal import Decimal
# import yaml
from utils.helper import fetch_bank_config, get_tagging_rules
from models.transaction import Transaction, TransactionType
from services.api_client import insert_transactions

class DataHandling:
    def __init__(self, bank:str, statement_path:str):
        self.bank = bank
        self.statement_path = statement_path
        self.bank_config = fetch_bank_config(self.bank)
        self._tagging_rules = None  # Cache tagging rules
    
    @property
    def tagging_rules(self):
        """Lazy load and cache tagging rules"""
        if self._tagging_rules is None:
            print("Fetching tagging rules from API...")
            self._tagging_rules = get_tagging_rules()
        return self._tagging_rules

    def load_excel_statement(self) -> pd.DataFrame:
        if self.bank_config is None:
            raise ValueError(f"Bank configuration not found for {self.bank}")
        
        try:
            df = pd.read_excel(
                self.statement_path,
                skiprows = self.bank_config["skiprows"],
                skipfooter = self.bank_config["skipfooter"],
                usecols = self.bank_config["usecols"],
                engine = self.bank_config["engine"]
            )
            print(f"Loaded {len(df)} rows from statement")
            return df
        except Exception as e:
            raise Exception(f"Error reading Excel file: {str(e)}")

    def clean_description(self, desc: str) -> str:
        reason = desc
        if desc.startswith('UPI'):
            reason = desc.split('-')[-1]
        if 'UPI' not in reason and not "PAY" in reason: return reason
        return desc

    def clean_statement(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.bank_config is None:
            raise ValueError(f"Bank configuration not found for {self.bank}")
        
        try:
            # Rename columns according to bank config
            df = df.rename(columns=self.bank_config["column_mapping"])
            
            # Remove completely empty rows
            df = df.dropna(how="all")
            
            # Clean description field and store original
            if "description" in df.columns:
                # Store original description before cleaning
                df["old_description"] = df["description"].str.strip()
                df["description"] = df["description"].str.strip().str.upper().apply(self.clean_description)
            
            # Convert date column
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                df = df.dropna(subset=["date"])
            
            # Handle amount columns
            if "withdrawal" in df.columns:
                df["withdrawal"] = pd.to_numeric(df["withdrawal"], errors="coerce").fillna(0)
            if "deposit" in df.columns:
                df["deposit"] = pd.to_numeric(df["deposit"], errors="coerce").fillna(0)
            
            # Calculate net amount and transaction type
            if "withdrawal" in df.columns and "deposit" in df.columns:
                df["amount"] = df["deposit"] - df["withdrawal"]
                df["type"] = df["amount"].apply(lambda x: "credit" if x > 0 else "debit")
                df = df.drop(columns=["withdrawal", "deposit"])
            
            df["bank"] = self.bank
            print(f"Cleaned statement: {len(df)} valid transactions")
            return df
        except Exception as e:
            raise Exception(f"Error cleaning statement data: {str(e)}")

    def get_tag(self, desc: str) -> tuple:
        """
        Get tag for a transaction description.
        Returns tuple of (tag_name, tag_id)
        """
        try:
            # Use cached tagging rules instead of fetching every time
            tagging_rules = self.tagging_rules
            
            # Find matching rule for description using 'keyword' field
            desc_upper = desc.upper()
            for rule in tagging_rules:
                keyword = rule.get('keyword', '').strip().upper()
                if keyword and keyword in desc_upper:
                    # Debug: print matched tag for first few transactions
                    if hasattr(self, '_debug_count') and self._debug_count < 3:
                        print(f"Matched '{keyword}' in '{desc}' -> {rule.get('tag_name')}")
                        self._debug_count += 1
                    elif not hasattr(self, '_debug_count'):
                        self._debug_count = 1
                        print(f"Matched '{keyword}' in '{desc}' -> {rule.get('tag_name')}")
                    return (
                        rule.get('tag_name', 'Unknown'),
                        rule.get('tag_id', None)
                    )
            
            # No matching rule found
            return ('Unknown', None)
        except Exception as e:
            print(f"Error in get_tag: {str(e)}")
            return ('Unknown', None)

    def apply_tags(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply tags to transactions based on description.
        """
        if "description" not in df.columns:
            print("Warning: No description column found for tagging")
            df["tag_name"] = "Unknown"
            df["tag_id"] = None
            return df
        
        # Apply tagging rules
        tagging_results = df["description"].apply(self.get_tag)
        
        # Split tuple results into separate columns
        df[["tag_name", "tag_id"]] = pd.DataFrame(
            tagging_results.tolist(), index=df.index
        )
        
        print(f"Applied tags to {len(df)} transactions")
        return df
    
    def dataframe_to_transactions(self, df: pd.DataFrame, user_id: int, acc_id: int) -> List[Transaction]:
        """
        Convert processed DataFrame to Transaction objects.
        """
        transactions = []
        
        for _, row in df.iterrows():
            try:
                # Generate reference ID if not present
                ref_id = row.get('reference_id', f"{self.bank}_{row.get('date', datetime.now()).strftime('%Y%m%d')}_{len(transactions)}")
                
                # Convert type to TransactionType enum
                transaction_type = TransactionType.CREDIT if row.get('type', 'debit') == 'credit' else TransactionType.DEBIT
                
                transaction = Transaction(
                    transaction_id=None,
                    transaction_time=pd.to_datetime(row['date']).to_pydatetime(),  # Convert to Python datetime
                    description=row.get('description', ''),
                    old_description=row.get('old_description', row.get('description', '')),
                    amount=Decimal(str(row['amount'])),  # Convert to Decimal
                    reference_id=str(ref_id),
                    type=transaction_type,
                    created_at=None,
                    modified_at=None,
                    tag_id=None if pd.isna(row.get('tag_id', None)) else int(row.get('tag_id', 0)) if row.get('tag_id') else None,
                    acc_id=acc_id,
                    user_id=user_id
                )
                transactions.append(transaction)
            except Exception as e:
                print(f"Error converting row to transaction: {str(e)}")
                continue
        
        print(f"Converted {len(transactions)} rows to Transaction objects")
        return transactions
    
    def process_and_upload_statement(self, user_id: int, acc_id: int) -> dict:
        """
        Complete pipeline to process statement and upload to backend.
        """
        try:
            # Load statement
            print(f"Loading statement from {self.statement_path}")
            df = self.load_excel_statement()
            
            # Clean statement data
            print("Cleaning statement data...")
            df = self.clean_statement(df)
            
            # Apply tagging rules
            print("Applying tagging rules...")
            df = self.apply_tags(df)
            
            # Convert to Transaction objects
            print("Converting to Transaction objects...")
            transactions = self.dataframe_to_transactions(df, user_id, acc_id)
            
            if not transactions:
                return {"success": False, "message": "No valid transactions found"}
            
            # Upload to backend
            print(f"Uploading {len(transactions)} transactions...")
            result = insert_transactions(transactions)
            
            return {
                "success": True, 
                "message": f"Successfully processed {len(transactions)} transactions",
                "result": result
            }
            
        except Exception as e:
            error_msg = f"Error processing statement: {str(e)}"
            print(error_msg)
            return {"success": False, "message": error_msg}
