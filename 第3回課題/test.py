import flet as ft
from library.backend.db.select import select_area_code, select_office_code

office_code = "0"
office_dropdown = None

def on_change_area_dropdown(e, page):
    global office_code, office_dropdown
    print(e.data)
    office_code = e.data
    office_dropdown.options = [
        ft.dropdown.Option(key, value) for key, value, _ in select_office_code(office_code)
    ]
    office_dropdown.update()
    page.update()
    print("update_dropdown")

def on_change_office_dropdown(e):
    print(e.data)

# 地方選択用ドロップダウン
def craft_area_dropdown(page):
    area_dropdown = ft.Dropdown(
        ref=select_area_code,
        options=[
            ft.dropdown.Option(key, value) for key, value, _ in select_area_code()
        ],
        label="地方を選択してください",
        on_change=lambda e: on_change_area_dropdown(e, page),
    )
    return area_dropdown

# 地域選択用ドロップダウン
def craft_office_dropdown():
    global office_code
    print(office_code, "office_code")
    office_dropdown = ft.Dropdown(
        ref=select_office_code,
        options=[
            ft.dropdown.Option(key, value) for key, value, _ in select_office_code(office_code)
        ],
        label="地域を選択してください",
        on_change=on_change_office_dropdown,
    )
    return office_dropdown

def main(page: ft.Page):
    global office_dropdown
    page.title = "天気予報アプリ"
    page.padding = 20 # 余白
    page.spacing = 20 # 間隔
    area_dropdown = craft_area_dropdown(page)
    office_dropdown = craft_office_dropdown()
    page.add(
        ft.Column(
            [
                ft.Text("天気予報アプリ", size=30 ,weight="bold"),
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("column", size=30 ,weight="bold"), 
                                ft.Text("天気予報アプリ", size=30 ,weight="bold"),
                                area_dropdown,
                                office_dropdown,
                            ],
                            scroll=True,
                        ),
                        ft.Text("row", size=30 ,weight="bold"),
                    ],
                    scroll=True,
                ),
            ],
            scroll=True,
        ),
    )

ft.app(target=main)