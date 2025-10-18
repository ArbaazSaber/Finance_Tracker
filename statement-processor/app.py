from services.processor import DataHandling

if __name__ == "__main__":
    file_path = "D:\\Downloads\\Oct2024-Oct2025.xls"
    bank_name = "HDFC"

    hdfc_bank = DataHandling(bank_name, file_path)
    df = hdfc_bank.load_excel_statement()
    print(df.head())
    with open("check_df.txt", "w") as f:
        f.write(df.to_string())
    df = hdfc_bank.clean_statement(df)
    with open("check_df_after_clean.txt", "w") as f:
        f.write(df.to_string())
    # print(df)