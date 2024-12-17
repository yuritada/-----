import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from library.config import DB_PATH
from library.backend.db.connection import get_connection, close_connection
from library.backend.db.insert import insert_weather_day_data, insert_weather_day_pops_data, insert_weather_day_temps_data
from library.backend.request.request import request_weather_data
from library.backend.request.adjust import adjust_weather_data_for_weather_day_table, adjust_weather_data_for_weather_day_pops_table, adjust_weather_data_for_weather_day_temps_table


def request_adjust_insert(office_code):
    conn = get_connection(DB_PATH)
    cursor = conn.cursor()
    office_code, response = request_weather_data(office_code)
    for json in adjust_weather_data_for_weather_day_table(office_code,response):
        try:
            insert_weather_day_data(cursor, json)
        except:
            pass
    for json in adjust_weather_data_for_weather_day_pops_table(office_code,response):
        try:
            insert_weather_day_pops_data(cursor, json)
        except:
            pass
    for json in adjust_weather_data_for_weather_day_temps_table(office_code,response):
        try:
            insert_weather_day_temps_data(cursor, json)
        except:
            pass
    conn.commit()
    close_connection(conn)

if __name__ == "__main__":
    request_adjust_insert("015000")

