import sqlite3

conn = sqlite3.connect("atm.db")
cur = conn.cursor()

cur.execute("""
INSERT INTO users (account_no, pin, name, balance)
VALUES (123456, 1234, 'Test User', 5000)
""")

conn.commit()
conn.close()

print("User added successfully")
