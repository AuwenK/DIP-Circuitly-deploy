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

CSV_PATH = Path(__file__).resolve().parent.parent / "scratch" / "lingo_quest" / "questions" / "QuestionBank_utf8.csv"

def map_difficulty(value: str) -> str:
    v = (value or "").strip().lower()
    if v in {"easy", "medium", "hard", "very hard"}:
        return v
    if v == "1":
        return "easy"
    if v == "2":
        return "medium"
    if v == "3":
        return "hard"
    if v == "4":
        return "very hard"
    return "medium"

def empty_to_none(value: str):
    if value is None:
        return None
    value = value.strip()
    return value if value else None

def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode="require",
    )

    inserted = 0

    try:
        with conn:
            with conn.cursor() as cur:
                # optional: clear staging and target if you want fresh import
                cur.execute("DELETE FROM questions;")

                with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
                    reader = csv.DictReader(f)
                    
                    for row in reader:
                        row_id = (row.get("id") or "").strip()
                        topic_id = (row.get("topicId") or "").strip()
                        question = (row.get("question") or "").strip()

                        # Skip rows with missing required identifiers or text
                        if not row_id or not topic_id or not question:
                            print(f"Skipping row with missing ID/Topic/Question: ID={row_id}")
                            continue
                        
                        answer = (row.get("answer") or "").strip()
                        if not answer:
                            print(f"Skipping row with missing answer: ID={row_id}")
                            continue

                        try:
                            q_id = int(row_id)
                            t_id = int(topic_id)
                        except ValueError:
                            print(f"Skipping row with malformed integer IDs: ID={row_id}, Topic={topic_id}")
                            continue

                        cur.execute(
                            """
                            INSERT INTO questions (
                                id,
                                topic_id,
                                type,
                                difficulty,
                                prompt,
                                option_a,
                                option_b,
                                option_c,
                                option_d,
                                answer,
                                image_url,
                                explanation
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                q_id,
                                t_id,
                                "mcq",
                                map_difficulty(row.get("difficulty", "")),
                                question,
                                empty_to_none(row.get("optionA")),
                                empty_to_none(row.get("optionB")),
                                empty_to_none(row.get("optionC")),
                                empty_to_none(row.get("optionD")),
                                answer,
                                empty_to_none(row.get("image")),
                                empty_to_none(row.get("explanation")),
                            ),
                        )
                        inserted += 1

        print(f"Import complete. Inserted {inserted} rows into questions.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()