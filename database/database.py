import sqlite3

DATABASE = "tasks.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due_date TEXT,
            due_time TEXT,
            priority TEXT DEFAULT 'NORMAL',
            category TEXT DEFAULT 'General',
            status TEXT DEFAULT 'PENDING',
            reminder_enabled INTEGER DEFAULT 0,
            reminder_sent INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()