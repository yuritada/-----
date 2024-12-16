def craft_area_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS area (
        area_id INTEGER PRIMARY KEY AUTOINCREMENT, -- 主キー
        area_class TEXT NOT NULL, -- centers, offices
        area_num TEXT NOT NULL, -- エリアコード
        area_name TEXT NOT NULL, -- 地名
        area_enname TEXT, -- 地名（英語）
        area_officename TEXT, -- 気象台の名前
        area_parents INTEGER -- “parents”項目
    )
    ''')

def craft_weather_code_mapping_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_code_mapping (
        weather_code INTEGER PRIMARY KEY, -- 天気コード
        morning_mark TEXT, -- 昼のマーク(.svgまで含む)
        evening_mark TEXT, -- 夜のマーク(.svgまで含む)
        short_name TEXT, -- 天気の名称(表示用に短く)
        en_name TEXT -- 天気の英語名称
    )
    ''')

def craft_weather_day_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_day (
        weather_day_id INTEGER PRIMARY KEY AUTOINCREMENT, -- 主キー
        office_code TEXT NOT NULL, -- エリアコード        
        area_name TEXT NOT NULL, -- 地域名
        report_datetime TEXT NOT NULL, -- 予報発表時間
        time_defines TEXT NOT NULL, -- 予報対象時間
        weather_code INTEGER NOT NULL, -- 天気コード
        weather_name TEXT, -- 天気名(short_name)
        wind TEXT, -- 風の方向
        wave TEXT, -- 波の高さ（欠損値あり）
        FOREIGN KEY (weather_code) REFERENCES weather_code_mapping (weather_code),
        UNIQUE (office_code, area_name, report_datetime, time_defines, weather_code, weather_name, wind, wave)
    )
    ''')

# def craft_weather_day_pops_table(cursor):
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS weather_day_pops (
#         id INTEGER PRIMARY KEY AUTOINCREMENT, -- 主キー
#         office_code TEXT NOT NULL, -- エリアコード
#         area_name TEXT NOT NULL, -- 地域名
#         report_datetime TEXT NOT NULL, -- 予報発表時間
#         time_defines TEXT NOT NULL, -- 予報対象時間
#         pop INTEGER NOT NULL -- 降水確率
#     )
#     ''')

def craft_weather_day_pops_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_day_pops (
        weather_day_pops_id INTEGER PRIMARY KEY AUTOINCREMENT, -- 主キー
        office_code TEXT NOT NULL, -- エリアコード  
        area_name TEXT NOT NULL, -- 地域名
        report_datetime TEXT NOT NULL, -- 予報発表時間
        time_defines TEXT NOT NULL, -- 予報対象時間
        pops INTEGER NOT NULL, -- 降水確率
        UNIQUE (office_code, area_name, report_datetime, time_defines, pops)
    )
    ''')


# def craft_weather_day_temps_table(cursor):
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS weather_day_temps (
#         weather_day_temps_id INTEGER PRIMARY KEY AUTOINCREMENT, -- 主キー
#         office_code TEXT NOT NULL, -- エリアコード  
#         area_name TEXT NOT NULL, -- 地域名
#         report_datetime TEXT NOT NULL, -- 予報発表時間
#         time_defines TEXT NOT NULL, -- 予報対象時間
#         temps INTEGER, -- 気温
#         UNIQUE (office_code, area_name, report_datetime, time_defines, temps)
#     )
#     ''')
def craft_weather_day_temps_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_day_temps (
        weather_day_temps_id INTEGER PRIMARY KEY AUTOINCREMENT, -- 主キー
        office_code TEXT NOT NULL, -- エリアコード  
        area_name TEXT NOT NULL, -- 地域名
        report_datetime TEXT NOT NULL, -- 予報発表時間
        time_defines TEXT NOT NULL, -- 予報対象時間
        temps INTEGER, -- 気温
        UNIQUE (office_code, area_name, report_datetime, time_defines, temps)
    )
    ''')
