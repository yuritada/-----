import os

def get_absolute_path(relative_path):
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


relative_path = 'asset/weather.db'
DB_PATH = get_absolute_path(relative_path)
area_data_path = 'asset/area.json'
AREA_PATH = get_absolute_path(area_data_path)
weather_data_path = 'asset/weather_data.json'
WEATHER_PATH = get_absolute_path(weather_data_path)