from services.processor import DataHandling

if __name__ == "__main__":
    file_path = "D:\\Downloads\\Oct2024-Oct2025.xls"
    bank_name = "HDFC"
    user_id = 1  # TODO: Make this configurable
    acc_id = 1   # TODO: Make this configurable

    try:
        hdfc_bank = DataHandling(bank_name, file_path)
        df = hdfc_bank.load_excel_statement()
        print(df.head())
        # with open("check_df.txt", "w") as f:
        #     f.write(df.to_string())
        df = hdfc_bank.clean_statement(df)
        # with open("check_df_after_clean.txt", "w") as f:
        #     f.write(df.to_string())
        
        # Apply tagging and process transactions
        df = hdfc_bank.apply_tags(df)
        
        # Process and upload transactions using bulk API
        result = hdfc_bank.process_and_upload_statement(user_id, acc_id)
        
        if result['success']:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ {result['message']}")
            
    except Exception as e:
        print(f"❌ Error processing statement: {str(e)}")
