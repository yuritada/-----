"""これ英語バージョンも作れるっっっっっぞ!!!! area.jsonにenNameがあるからな"""


import flet as ft
from backend import back
from yazirushi import make_yazirushi
from hogehoge import *

def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.padding = 20
    page.spacing = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # backクラスの初期化
    object = back("area.json", "response.json")
    areas = object.load_area_codes()  # 地方コードをロード
    office = { None :{"name": "地域を選択してください" }}
    weather = { None :{"name": "天気情報がここに表示されます。" }}

    # コンポーネントの初期化
    selected_area_code = ft.Ref[ft.Dropdown]()
    selected_office_code = ft.Ref[ft.Dropdown]()
    result_output = ft.Ref[ft.Text]()
       
    def get_office_codes(e):
        global office
        office = object.load_office_codes(selected_area_code.current.value)  # 地域コードをロード
        # 関数内の参照を更新（再定義）
        office_dropdown.options = [
            ft.dropdown.Option(key, value) for key, value in office.items()
        ]
        # 表示の更新
        page.update()

    def get_weather_data(e):
        global weather
        weather = object.fetch_weather_data(selected_office_code.current.value)
        # 関数内の参照を更新（再定義）
        result_text.value = object.format_data_days()
        # 表示の更新
        page.update()


    # 地方選択用ドロップダウン
    area_dropdown = ft.Dropdown(
        ref=selected_area_code,
        options=[
            ft.dropdown.Option(key, value) for key, value in areas.items()
        ],
        label="地方を選択してください",
        on_change = get_office_codes,
    )

    # 地域選択用ドロップダウン
    office_dropdown = ft.Dropdown(
        ref=selected_office_code,
        options=[
            ft.dropdown.Option(key, value) for key, value in office.items()
        ],
        label="地域を選択してください",
        on_change = get_weather_data,
    )

    # 結果表示用テキスト
    result_text = ft.Text(
        ref=result_output,
        value=(object.format_data_days()),
        selectable=True,
        size=16,
    )

    cards = generate_weather_cards(object.format_data_days())

    # ページにコンポーネントを追加
    page.add(
        ft.Column(
            [
                ft.Text("天気予報アプリ", size=30 ,weight="bold"),
                ft.Row(
                    [
                        ft.Column(
                            [
                                area_dropdown,
                                office_dropdown,
                            ],
                            scroll=True,
                        ),
                        cards,
                    ],
                    scroll=True,
                    alignment="center",
                ),
            ],
            scroll=True,
        ),
    )

# Fletアプリケーションを起動
if __name__ == "__main__":
    ft.app(target=main)