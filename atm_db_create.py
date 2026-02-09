import sqlite3

conn = sqlite3.connect("atm.db")
cursor = conn.cursor()

# Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    account_no TEXT,
    pin TEXT,
    balance REAL
)
''')

# Transactions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT,
    amount REAL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Demo user
cursor.execute('''
INSERT INTO users (name, account_no, pin, balance)
VALUES ('Vicky Bhagat', '123456', '1234', 10000)
''')

conn.commit()
conn.close()

print("SQLite database ready ✅")