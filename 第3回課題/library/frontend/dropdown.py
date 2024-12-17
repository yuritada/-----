import flet as ft
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from library.backend.db.select import select_area_code, select_office_code, select_report_time
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

def on_change_office_dropdown(e, page):
    request_adjust_insert(f"{e.data}")
    page.update()
    print("やったぜ")

def on_change_type_dropdown(e, page):
    global select_type, type_dropdown
    select_type = e.data
    type_dropdown.options=[
            ft.dropdown.Option(key, value) for key, value in select_report_time(e.data, office_code)
        ]
    type_dropdown.update()
    print(select_type,e.data,office_code)
    page.update()

def on_change_reporttime_dropdown(e, page):
    global select_time
    select_time = e.data
    print(e.data)
    page.update()


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
    global select_type_code
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
    global type_dropdown
    type_dropdown = ft.Dropdown(
        ref=select_report_time,
        options=[
            ft.dropdown.Option(key, value) for key, value in select_report_time(select_type, office_code)
        ],
        label="予報タイプを選択してください",
        on_change=lambda e: on_change_reporttime_dropdown(e, page),
    )
    return type_dropdown