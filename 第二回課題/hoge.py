import flet as ft
import json
from backend import back
from yazirushi import make_yazirushi

# 天気カード生成関数の強化版
def create_weather_card(date, area_name, weather, weather_image_url, wind, wave, temperature_min, temperature_max):
    wave_row = None
    if wave != 0:
        wave_row = ft.Row(
            [
                ft.Text("波高", size=12),
                ft.Text(str(wave), size=12),  # 数値を文字列に変換
            ],
            alignment="center",
        )

    content_items = [
        ft.Text(date, size=14, weight="bold"),
        ft.Text(area_name, size=12, color=ft.colors.GREY),
        ft.Image(src=weather_image_url, width=50, height=50, fit=ft.ImageFit.CONTAIN),
        ft.Text(weather, size=12),
        ft.Text(f"風速: {wind}", size=12),
        make_yazirushi(wind),  # 風速に関連する表示を追加
        ft.Text(f"気温: {temperature_min}°C - {temperature_max}°C", size=12),
    ]

    if wave_row is not None:
        content_items.append(wave_row)

    return ft.Container(
        content=ft.Column(
            content_items,
            alignment="center",
            horizontal_alignment="center",
        ),
        width=180,  # 少し大きめに調整
        height=350,  # 高さを調整
        border=ft.border.all(1, ft.colors.GREY),
        border_radius=ft.border_radius.all(10),
        padding=10,
        margin=ft.margin.all(10),
        bgcolor=ft.colors.LIGHT_BLUE_50,  # 背景色を追加して、視認性を向上
    )

# カード生成のロジックを活用して、複数のカードを作成
def generate_weather_cards(data):
    cards = []
    for key, weather_info in data.items():
        try:
            if weather_info["weather_code"]:
                date = weather_info["day"]
                area_name = weather_info["area_name"]
                weather = weather_data[weather_info["weather_code"]]["short_name"]
                weather_image_url = create_link(weather_info["weather_code"], weather_info["Time"])
                wind = weather_info["wind"].split("の")[0]
                try:
                    wave = weather_info["wave"].split(" 後")[0]
                except:
                    wave = 0
                temperature_min = weather_info.get("temps_Min", "N/A")
                temperature_max = weather_info.get("temps_Max", "N/A")
                cards.append(create_weather_card(date, area_name, weather, weather_image_url, wind, wave, temperature_min, temperature_max))
        except:
            pass
    return cards

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
    result_output = ft.Ref[ft.Row]()
       
    def get_office_codes(e):
        global office
        office = object.load_office_codes(selected_area_code.current.value)  # 地域コードをロード
        office_dropdown.options = [
            ft.dropdown.Option(key, value) for key, value in office.items()
        ]
        page.update()

    def get_weather_data(e):
        global weather
        weather = object.fetch_weather_data(selected_office_code.current.value)
        result_output.value = object.format_data_days()
        cards = generate_weather_cards(weather)
        result_output.current.controls.clear()  # 既存のカードを削除
        result_output.current.controls.extend(cards)  # 新たに生成したカードを追加
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

    # 結果表示用Row (カードをここに配置)
    result_row = ft.Row(
        ref=result_output,
        spacing=10,
        alignment="center",
    )

    page.add(
        ft.Column(
            [
                ft.Text("天気予報アプリ", size=30, weight="bold"),
                ft.Row(
                    [
                        ft.Column(
                            [
                                area_dropdown,
                                office_dropdown,
                            ],
                            scroll=True,
                        ),
                        result_row,
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