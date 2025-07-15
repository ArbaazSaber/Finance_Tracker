import db.database as db_conn
from utils.logger import logger

def get_bank_id(bank_name: str) -> int:
    bank_name = bank_name.strip()

    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT bank_id FROM banks WHERE bank_name = %s", (bank_name,))
        result = cursor.fetchone()

        if not result:
            raise ValueError(f"Bank {bank_name} does not exist")
        bank_id = result[0]

        print(f"Bank - {bank_name} with ID - {bank_id}")
        return bank_id
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_bank_name(bank_id: int) -> str:
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT bank_name FROM banks WHERE bank_id = %s", (bank_id,))
        result = cursor.fetchone()

        if not result:
            raise ValueError(f"Bank {bank_id} does not exist")
        bank_name = result[0]

        print(f"Bank - {bank_name} with ID - {bank_id}")

        return bank_name
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_all_banks() -> list:
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM banks;")
        result = cursor.fetchall()

        if not result:
            raise ValueError(f"Bank Table Empty!")

        banks = [(bank[0], bank[1]) for bank in result]

        print(f"Banks - {banks}")
        
        return banks
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_all_bank_names() -> list:
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT bank_name FROM banks ORDER BY bank_name;")
        result = cursor.fetchall()

        if not result:
            raise ValueError(f"Bank Table Empty!")

        bank_names = [bank[0] for bank in result]

        print(f"Banks - {bank_names}")
        
        return bank_names
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_all_bank_ids() -> list:
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT bank_id FROM banks;")
        result = cursor.fetchall()

        if not result:
            raise ValueError(f"Bank Table Empty!")

        bank_ids = [bank[0] for bank in result]

        print(f"Bank IDs - {bank_ids}")
        
        return bank_ids
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def insert_bank(bank_name: str) -> int:
    bank_name = bank_name.strip()

    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO banks (bank_name) VALUES (%s) RETURNING bank_id;", (bank_name,))
        bank_id = cursor.fetchone()[0]
        conn.commit()

        print(f"Inserted Bank: {bank_name} with ID: {bank_id}")

        return bank_id
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        
def does_bank_exist(bank_name: str) -> bool:
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM banks WHERE bank_name = %s", (bank_name,))
        result = cursor.fetchone()
        if not result:
            return False
        return True
    except Exception as e:
        print("Error: ",e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def count_banks() -> int:
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM banks")
        result = cursor.fetchone()
        if not result:
            return 0
        return result[0]
    except Exception as e:
        print("Error: ",e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_latest_bank_entry() -> str:
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT bank_name FROM banks ORDER BY bank_id DESC LIMIT 1")
        result = cursor.fetchone()
        if not result:
            return None
        return result[0]
    except Exception as e:
        print("Error: ",e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def get_banks_without_rules():
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT b.bank_name FROM banks b WHERE NOT EXISTS ( SELECT 1 FROM bank_rules br WHERE br.bank_id = b.bank_id ) ORDER BY b.bank_name")
        bank_names = cursor.fetchall()

        result = [bank_name[0] for bank_name in bank_names]
        print(f"Banks - {result}")
        
        return result
    except Exception as e:
        print("Error: ", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()