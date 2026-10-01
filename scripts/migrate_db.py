import sqlite3
from pathlib import Path

DB_PATH = Path("data/app.db")

def migrate():
    if not DB_PATH.exists():
        print("Database file data/app.db does not exist yet.")
        return

    print(f"🔧 Running Database Migration on: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Check users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        role TEXT DEFAULT 'student',
        department TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Check subjects columns for user_id
    cursor.execute("PRAGMA table_info(subjects)")
    subj_cols = [row[1] for row in cursor.fetchall()]
    if "user_id" not in subj_cols:
        print("➕ Adding missing column 'user_id' to 'subjects' table...")
        cursor.execute("ALTER TABLE subjects ADD COLUMN user_id INTEGER REFERENCES users(id);")

    # 3. Check chats columns for user_id
    cursor.execute("PRAGMA table_info(chats)")
    chat_cols = [row[1] for row in cursor.fetchall()]
    if "user_id" not in chat_cols:
        print("➕ Adding missing column 'user_id' to 'chats' table...")
        cursor.execute("ALTER TABLE chats ADD COLUMN user_id INTEGER REFERENCES users(id);")

    conn.commit()
    conn.close()
    print("✅ Database Migration Completed Successfully!")

if __name__ == "__main__":
    migrate()
