from typing import Dict, List  # Added for type hinting

from loguru import logger  # Added loguru import

from .database import get_connection


def create_upi(name: str, upi_id: str) -> None:  # Added type hint
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO upi (name, upi_id) VALUES (%s, %s)"
            cursor.execute(sql, (name, upi_id))
        conn.commit()
    except Exception as e:
        logger.error(
            f"[CRUD ERROR] Failed to create UPI: {e}"
        )  # Replaced print with logger
        raise
    finally:
        conn.close()


def get_all_upi() -> List[Dict]:  # Added type hint
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM upi")
            return cursor.fetchall()
    finally:
        conn.close()


def update_upi(id: int, name: str, upi_id: str) -> None:  # Added type hint
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE upi SET name=%s, upi_id=%s WHERE id=%s"
            cursor.execute(sql, (name, upi_id, id))
        conn.commit()
    finally:
        conn.close()


def delete_upi(id: int) -> None:  # Added type hint
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM upi WHERE id=%s"
            cursor.execute(sql, (id,))
        conn.commit()
    finally:
        conn.close()
