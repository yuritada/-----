import sqlite3

def get_connection(db_path):
    return sqlite3.connect(db_path)

def close_connection(conn):
    conn.close()
