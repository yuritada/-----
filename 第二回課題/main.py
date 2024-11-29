import flet as ft
from request import WeatherAPI  # 作成したバックエンドクラスをインポート

def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.padding = 20
    page.spacing = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # WeatherAPIクラスの初期化
    weather_api = WeatherAPI("area.json", "response.json")
    areas = weather_api.load_area_codes()  # 地方コードをロード
    office = weather_api.load_area_codes()  # 地域コードをロード

    # コンポーネントの初期化
    selected_area_code = ft.Ref[ft.Dropdown]()
    selected_office_code = ft.Ref[ft.Dropdown]()
    result_output = ft.Ref[ft.Text]()

    # 地域選択用ドロップダウン
    area_dropdown = ft.Dropdown(
        ref=selected_area_code,
        options=[
            ft.dropdown.Option(key, value["name"])
            for key, value in areas.items()
        ],
        label="地方を選択してください",
    )

    # 地域選択用ドロップダウン
    office_dropdown = ft.Dropdown(
        ref=selected_office_code,
        options=[
            ft.dropdown.Option(key, value["name"])
            for key, value in office.items()
        ],
        label="地域を選択してください",
    )

    # 結果表示用テキスト
    result_text = ft.Text(
        ref=result_output,
        value="天気情報がここに表示されます。",
        selectable=True,
        size=16,
    )

    # データ取得ボタン
    def fetch_weather_data(e):
        if selected_area_code.current.value:
            area_code = selected_area_code.current.value
            try:
                # 天気データを取得し、パースして表示
                weather_data = weather_api.fetch_weather_data(area_code)
                parsed_data = weather_api.parse_weather_data(weather_data, area_code)
                # データを整形して表示
                result_output.current.value = f"""
                地域: {areas[area_code]["name"]}
                発表者: {parsed_data["publishingOffice"]}
                発表日時: {parsed_data["reportDatetime"]}
                天気: {parsed_data["weather"]}
                風: {parsed_data["wind"]}
                波: {parsed_data["wave"]}
                """
            except Exception as ex:
                result_output.current.value = f"エラーが発生しました: {ex}"
            page.update()
        else:
            result_output.current.value = "地域を選択してください。"
            page.update()

    fetch_button = ft.ElevatedButton(
        text="天気を取得する", on_click=fetch_weather_data
    )

    # ページにコンポーネントを追加
    page.add(
        ft.Column(
            [
                ft.Text("天気予報アプリ", size=30, weight="bold"),
                area_dropdown,
                office_dropdown,
                fetch_button,
                result_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

# Fletアプリケーションを起動
if __name__ == "__main__":
    ft.app(target=main)