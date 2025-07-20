import db.database as db_conn
import utils.util_functions as utils
from utils.logger import logger

def get_category_id(category_name: str) -> int:
    category_name = utils.format_string(category_name)

    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT category_id FROM categories WHERE category_name = %s", (category_name,))
        result = cursor.fetchone()

        if not result:
            raise ValueError(f"Category {category_name} does not exist")
        category_id = result[0]

        logger.info("Category - {category_name} with ID - {category_id}")
        return category_id
    except Exception as e:
        logger.exception(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_category_name(category_id: int) -> str:
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT category_name FROM categories WHERE category_id = %s", (category_id,))
        result = cursor.fetchone()

        if not result:
            raise ValueError(f"Category {category_id} does not exist")
        category_name = result[0]

        logger.info("Category - {category_name} with ID - {category_id}")

        return category_name
    except Exception as e:
        logger.exception(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def get_all_categories() -> list:
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM categories;")
        result = cursor.fetchall()

        if not result:
            raise ValueError(f"Category Table Empty!")

        categories = [(category[0], category[1]) for category in result]

        logger.info("Categories - {categories}")
        
        return categories
    except Exception as e:
        logger.exception(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_all_category_names() -> list:
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT category_name FROM categories ORDER BY category_name;")
        result = cursor.fetchall()

        if not result:
            raise ValueError(f"Category Table Empty!")

        category_names = [category[0] for category in result]

        logger.info("Categories - {category_names}")
        
        return category_names
    except Exception as e:
        logger.exception(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_all_category_ids() -> list:
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT category_id FROM categories;")
        result = cursor.fetchall()

        if not result:
            raise ValueError(f"Category Table Empty!")

        category_ids = [category[0] for category in result]

        logger.info("Category IDs - {category_ids}")
        
        return category_ids
    except Exception as e:
        logger.exception(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def insert_category(category_name: str):
    category_name = utils.format_string(category_name)

    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO categories (category_name) VALUES (%s) RETURNING category_id;", (category_name,))
        category_id = cursor.fetchone()[0]
        conn.commit()

        logger.info("Inserted Category: {category_name} with ID: {category_id}")
    except Exception as e:
        logger.exception(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

        
def does_category_exist(category_name: str) -> bool:
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM categories WHERE category_name = %s", (category_name,))
        result = cursor.fetchone()
        if not result:
            return False
        return True
    except Exception as e:
        logger.exception(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def count_categories() -> int:
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM categories")
        result = cursor.fetchone()
        if not result:
            return 0
        return result[0]
    except Exception as e:
        logger.exception(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def get_latest_category_entry() -> str:
    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT category_name FROM categories ORDER BY category_id DESC LIMIT 1")
        result = cursor.fetchone()
        if not result:
            return None
        return result[0]
    except Exception as e:
        logger.exception(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
        
if __name__ == "__main__":
    logger.info(get_all_categories())
    logger.info(get_all_category_ids())
    logger.info(get_all_category_names())
    logger.info(get_latest_category_entry())
    logger.info(does_category_exist("Needs"))
    logger.info(does_category_exist("Need"))
    logger.info(count_categories())