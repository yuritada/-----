import sqlite3

def create_database(db_name):
    """
    データベースとテーブルを作成する
    :param db_name: データベースのファイル名
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # テーブル作成
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_name TEXT NOT NULL,
        distance INTEGER NOT NULL,
        age INTEGER NOT NULL,
        price INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def insert_data(db_name, data):
    """
    データをデータベースに挿入する
    :param db_name: データベースのファイル名
    :param data: [(room_name, distance, age, price), ...] のリスト
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    for entry in data:
        cursor.execute('''
        INSERT INTO properties (room_name, distance, age, price) 
        VALUES (?, ?, ?, ?)
        ''', entry)
    conn.commit()
    conn.close()

def fetch_all_data(db_name):
    """
    データベースからすべてのデータを取得する
    :param db_name: データベースのファイル名
    :return: 全データ [(id, room_name, distance, age, price), ...] のリスト
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM properties')
    rows = cursor.fetchall()
    conn.close()
    return rows