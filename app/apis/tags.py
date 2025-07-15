import db.database as db_conn
import utils.util_functions as utils
import apis.categories as categories

def insert_tag(tag_name: str, category_name: str):
    tag_name = utils.format_string(tag_name)
    category_name = utils.format_string(category_name)

    try:
        conn = db_conn.get_connection()
        cursor = conn.cursor()

        category_id = categories.get_category_id(category_name)

        cursor.execute("INSERT INTO tags (tag_name, category_id) VALUES (%s,%s) RETURNING tag_id;", (tag_name, category_id))

        tag_id = cursor.fetchone()[0]
        conn.commit()

        print(f"Inserted tag: {tag_name} with ID: {tag_id}")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()