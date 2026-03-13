
import csv
import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

CSV_PATH = Path("c:/Users/65831/Downloads/DIP-Circuitly-main (2)/DIP-Circuitly-main/scratch/lingo_quest/questions/QuestionBank_utf8.csv")

def test_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            sslmode="require",
            connect_timeout=5
        )
        print("Database connection successful!")
        conn.close()
    except Exception as e:
        print(f"Database connection failed: {e}")

def test_csv_parsing():
    try:
        with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                count += 1
                if count <= 2:
                    print(f"Row {count}: {row}")
            print(f"Total rows parsed: {count}")
    except Exception as e:
        print(f"CSV parsing failed: {e}")

if __name__ == "__main__":
    print("Testing database connection...")
    test_db_connection()
    print("\nTesting CSV parsing...")
    test_csv_parsing()
