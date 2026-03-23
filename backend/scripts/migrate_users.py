import openpyxl
import bcrypt
import psycopg2
import os
import re
from dotenv import load_dotenv

# Path to the backend .env
ENV_PATH = r'C:/Users/rog/OneDrive/Desktop/DIP-Circuitly-deploy-main/DIP-Circuitly-deploy-main/backend/.env'
EXCEL_PATH = r'C:/Users/rog/OneDrive/Desktop/DIP-Circuitly-deploy-main/DIP-Circuitly-deploy-main/EE2101_25S2_IMPULSE_USERS.xlsx'

load_dotenv(ENV_PATH)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode="require"
    )

def migrate_users():
    conn = get_db_connection()
    cur = conn.cursor()
    
    wb = openpyxl.load_workbook(EXCEL_PATH)
    sheet = wb.active
    
    print("Starting migration...")
    count = 0
    for row in sheet.iter_rows(min_row=2, values_only=True):
        email = row[0]
        matrix_no = row[1]
        
        if not email or not matrix_no:
            continue
            
        email = str(email).strip().lower()
        matrix_no = str(matrix_no).strip().upper()
        
        # Simple name from email prefix
        name = email.split('@')[0].replace('.', ' ').title()
        
        # Hash matrix no
        password_hash = bcrypt.hashpw(matrix_no.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        try:
            cur.execute("""
                INSERT INTO users (username, password_hash, student_id, name, role)
                VALUES (%s, %s, %s, %s, 'user')
                ON CONFLICT (student_id) DO UPDATE SET
                    username = EXCLUDED.username,
                    password_hash = EXCLUDED.password_hash,
                    name = EXCLUDED.name,
                    last_active = NOW()
            """, (email, password_hash, matrix_no, name))
            count += 1
        except Exception as e:
            print(f"Failed to insert {email}: {e}")
            conn.rollback()
            continue
            
    conn.commit()
    cur.close()
    conn.close()
    print(f"Successfully migrated {count} users.")

if __name__ == "__main__":
    migrate_users()
