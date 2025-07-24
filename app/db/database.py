import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection(cursor_factory=None):
    return psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=cursor_factory)