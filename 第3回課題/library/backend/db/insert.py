def insert_area_data(cursor,clas,json,id):
    if clas == "centers":
        cursor.execute('''
        INSERT INTO area (area_class, area_num, area_name, area_enname, area_officename, area_parents) 
        VALUES (?,?,?,?,?,"null")
        ''',
        (clas, id, json["name"], json["enName"], json["officeName"]))
    elif clas == "offices": 
        cursor.execute('''
        INSERT INTO area (area_class, area_num, area_name, area_enname, area_officename, area_parents) 
        VALUES (?,?,?,?,?,?)
        ''',
        (clas, id, json["name"], json["enName"], json["officeName"], json["parent"]))
    else:
        cursor.execute('''
        INSERT INTO area (area_class, area_num, area_name, area_enname, area_officename, area_parents)
        VALUES (?,?,?,?,"null",?)
        ''',
        (clas, id, json["name"], json["enName"], json["parent"]))

def insert_weather_data(cursor,json,id):
        cursor.execute('''
        INSERT INTO weather_code_mapping (weather_code, morning_mark, evening_mark, short_name, en_name)
        VALUES (?,?,?,?,?)
        ''',
        (id ,json["morning_mark"], json["evening_mark"], json["short_name"], json["en_name"]))

def insert_weather_day_data(cursor,json):
    cursor.execute('''
    INSERT INTO weather_day (office_code, area_name, report_datetime, time_defines, weather_code, weather_name, wind, wave)
    VALUES (?,?,?,?,?,?,?,?)
    ''',
    (json["office_code"], json["area_name"], json["report_datetime"], json["time_defines"], json["weather_code"], json["weather_name"], json["wind"], json["wave"]))

def insert_weather_day_pops_data(cursor,json):
    cursor.execute('''
    INSERT INTO weather_day_pops (office_code, area_name, report_datetime, time_defines, pops)
    VALUES (?,?,?,?,?)
    ''',
    (json["office_code"], json["area_name"], json["report_datetime"], json["time_defines"], json["pops"]))

def insert_weather_day_temps_data(cursor,json):
    cursor.execute('''
    INSERT INTO weather_day_temps (office_code, area_name, report_datetime, time_defines, temps)
    VALUES (?,?,?,?,?)
    ''',
    (json["office_code"], json["area_name"], json["report_datetime"], json["time_defines"], json["temps"]))
