import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Sudipta@8350",
        database = "atm_db"
    )