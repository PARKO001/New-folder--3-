import os

import pymysql
from dotenv import load_dotenv
from pymysql.connections import Connection  # Added for type hint

load_dotenv()


def get_connection() -> Connection:  # Added type hint
    return pymysql.connect(
        host=os.getenv("DB_HOST") or "",
        user=os.getenv("DB_USER") or "",
        password=os.getenv("DB_PASSWORD") or "",
        database=os.getenv("DB_NAME") or "",
        cursorclass=pymysql.cursors.DictCursor,
    )
