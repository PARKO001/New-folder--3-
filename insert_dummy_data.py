import csv

from app.database import get_connection


def insert_dummy_data_from_csv(csv_path):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    sql = "INSERT INTO upi (name, upi_id) VALUES (%s, %s)"
                    cursor.execute(sql, (row["name"], row["upi_id"]))
        conn.commit()
        print("Dummy data inserted successfully.")
    except Exception as e:
        print(f"Error inserting dummy data: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    insert_dummy_data_from_csv("upi_dummy_data.csv")
