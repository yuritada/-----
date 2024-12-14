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
