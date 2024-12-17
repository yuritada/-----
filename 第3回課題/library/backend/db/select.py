import sqlite3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
from library.config import DB_PATH
from library.backend.db.connection import get_connection, close_connection

def select_full_table_data(clas):
    conn = get_connection(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {clas}")
    return_data = cursor.fetchall()
    close_connection(conn)
    return return_data

def select_area_code():
    conn = get_connection(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT area_num,area_name,area_enname FROM area WHERE area_class = 'centers'")
    return_data = cursor.fetchall()
    close_connection(conn)
    return return_data

def select_office_code(office_code):
    conn = get_connection(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT area_num,area_name,area_enname FROM area WHERE area_class = 'offices' AND area_parents = '{office_code}'")
    return_data = cursor.fetchall()
    close_connection(conn)
    return return_data

def select_report_time(table, office_code):
    conn = get_connection(DB_PATH)
    cursor = conn.cursor()
    print(table,office_code)
    cursor.execute(f"SELECT report_datetime FROM {table} WHERE office_code = '{office_code}'")
    return_data = cursor.fetchall()
    close_connection(conn)
    return return_data

def select_to_time(table, office_code, report_datetime):
    conn = get_connection(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT time_defines FROM {table} WHERE office_code = '{office_code}' AND report_datetime = '{report_datetime}'")
    return_data = cursor.fetchall()
    print(office_code,report_datetime,return_data)
    close_connection(conn)
    return return_data

def parent_area_code(area_code):
    return_data = []
    conn = get_connection(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT area_num,area_name FROM area WHERE area_parents = '{area_code}' and area_class = 'class10s'")
    return_data = cursor.fetchall()
    print(area_code,return_data)
    close_connection(conn)
    return return_data

def result_data(table, office_code, report_datetime, time_defines):
    return_data = []
    conn = get_connection(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE office_code = '{office_code}' AND report_datetime = '{report_datetime}' AND time_defines = '{time_defines}'")
    return_data = cursor.fetchall()
    close_connection(conn)
    return return_data

if __name__ == "__main__":
    # print(select_area_code())
    # print(select_office_code("010100"))
    # print(select_report_time("weather_day","010100"))
    print(parent_area_code("010100"))