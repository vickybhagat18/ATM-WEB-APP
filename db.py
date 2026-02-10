import sqlite3

def get_db_connection():
    conn = sqlite3.connect("atm.db")
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_no INTEGER UNIQUE,
        pin INTEGER,
        name TEXT,
        balance REAL
    )
    """)

    # transactions table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        amount REAL,
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # seed user (only if empty)
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO users (account_no, pin, name, balance) VALUES (?, ?, ?, ?)",
            (123456, 1234, "Test User", 5000)
        )

    conn.commit()
    conn.close()
