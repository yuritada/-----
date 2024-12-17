import flet as ft
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from library.backend.db.select import select_area_code, select_office_code, select_report_time, select_to_time, parent_area_code, result_data
from library.backend.main import request_adjust_insert

office_code = "0"
select_type = "weather_day"
select_type_code = [("weather_day", "天気"), ("weather_day_pops", "降水確率"), ("weather_day_temps", "気温")]
select_time = "0"
return_text_data = "こんにちは"

def on_change_area_dropdown(e, page):
    global office_code , office_dropdown
    print(e.data)
    office_code = e.data
    print(select_office_code(e.data))
    office_dropdown.options=[
            ft.dropdown.Option(key, value) for key, value, _ in select_office_code(e.data)
        ]
    office_dropdown.update()
    page.update()
    print(0)

def on_change_office_dropdown(e, page):
    global office_code, type_dropdown
    request_adjust_insert(f"{e.data}")
    detail_area_dropdown.options=[
            ft.dropdown.Option(key, value) for key, value in parent_area_code(e.data)
        ]
    print(parent_area_code(e.data))
    detail_area_dropdown.update()    
    page.update()
    print(1)

def on_change_detail_area(e, page):
    global office_code, office_dropdown, type_dropdown , detail_area_code
    detail_area_code = e.data
    type_dropdown.options=[
            ft.dropdown.Option(key, value) for key, value in select_type_code
        ]
    type_dropdown.update()
    page.update()
    print(2)

def on_change_type_dropdown(e, page):
    global select_type, type_dropdown, reporttime_dropdown
    select_type = e.data
    print(e.data,"aaaaaaaa")
    print(select_report_time(e.data, office_code))
    reporttime_dropdown.options=[
            ft.dropdown.Option(key, value) for key, value in select_report_time(e.data, office_code)
        ]
    reporttime_dropdown.update()
    page.update()
    print(3)

def on_change_reporttime_dropdown(e, page):
    global select_time, reporttime_dropdown, to_time_dropdown
    select_time = e.data
    to_time_dropdown.options=[
            ft.dropdown.Option(key, value) for key, value in select_to_time(select_type , office_code, e.data)
        ]
    to_time_dropdown.update()
    print(e.data)
    page.update()
    print(4)

def on_change_to_time(e, page):
    global to_time, to_time_dropdown,select_type, office_code, select_time ,detail_area_code
    to_time = e.data
    result_data(select_type, detail_area_code, select_time, to_time)
    print(e.data)
    page.update()
    print(5)

# 地方選択用ドロップダウン
def craft_area_dropdown(page):
    area_dropdown = ft.Dropdown(
        ref=select_area_code,
        options=[
            ft.dropdown.Option(key, value) for key, value, _ in select_area_code()
        ],
        label="地方を選択してください",
        on_change = lambda e: on_change_area_dropdown(e, page),
    )

    return area_dropdown

# 地域選択用ドロップダウン
def craft_office_dropdown(page):
    global office_code , office_dropdown
    print(office_code, "office_code")
    office_dropdown = ft.Dropdown(
        ref=select_office_code,
        options=[
            ft.dropdown.Option(key, value) for key, value,_ in select_office_code(office_code)
        ],
        label="地域を選択してください",
        on_change = lambda e: on_change_office_dropdown(e, page),
    )
    return office_dropdown

def craft_type_dropdown(page):
    global select_type_code, type_dropdown
    type_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option(key, value) for key, value in select_type_code
        ],
        label="予報タイプを選択してください",
        on_change=lambda e: on_change_type_dropdown(e, page),
        value="weather_day"
    )
    return type_dropdown

def craft_reporttime_dropdown(page):
    global reporttime_dropdown
    reporttime_dropdown = ft.Dropdown(
        ref=select_report_time,
        options=[
            ft.dropdown.Option(key, value) for key, value in select_report_time(select_type, office_code)
        ],
        label="発表日時を選択してください",
        on_change=lambda e: on_change_reporttime_dropdown(e, page),
    )
    return reporttime_dropdown

def craft_totime_dropdown(page):
    global to_time_dropdown
    to_time_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option(key, value) for key, value in select_to_time(select_type, office_code, select_time)
        ],
        label="発表対象日時を選択してください",
        on_change=lambda e: on_change_to_time(e, page),
    )
    return to_time_dropdown

def craft_detail_area_dropdown(page):
    global detail_area_dropdown, office_code
    detail_area_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option(key, value) for key, value,_ in parent_area_code(office_code)
        ],
        label="地区を選択してください",
        on_change = lambda e: on_change_detail_area(e, page),
    )

    return detail_area_dropdown