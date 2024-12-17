import sqlite3
import sys
from pathlib import Path
import json
from connection import get_connection, close_connection
from create import craft_area_table, craft_weather_code_mapping_table, craft_weather_day_table, craft_weather_day_pops_table, craft_weather_day_temps_table
from insert import insert_area_data, insert_weather_data
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
from library.config import DB_PATH, AREA_PATH, WEATHER_PATH

def __init__():
    global area_data, weather_data
    with open(AREA_PATH, "r") as f:
        area_data = json.load(f)
    with open(WEATHER_PATH, "r") as f:
        weather_data = json.load(f)

def initialize_db(db_path):
    global area_data, weather_data
    conn = get_connection(db_path)
    cursor = conn.cursor()
    craft_area_table(cursor)
    craft_weather_code_mapping_table(cursor)
    craft_weather_day_table(cursor)
    craft_weather_day_pops_table(cursor)
    craft_weather_day_temps_table(cursor)
    for clas in ["centers", "offices", "class10s", "class15s", "class20s"]:
        for id, data in area_data[clas].items():
            insert_area_data(cursor, clas, data, id)
    for id ,date in weather_data.items():
        insert_weather_data(cursor, date, id)
    conn.commit()
    close_connection(conn)

if __name__ == "__main__":
    __init__()
    initialize_db(DB_PATH)