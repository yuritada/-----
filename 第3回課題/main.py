import flet as ft
from library.frontend.dropdown import craft_area_dropdown, craft_office_dropdown, craft_type_dropdown, craft_reporttime_dropdown,return_text_data


def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.padding = 20 # 余白
    page.spacing = 20 # 間隔
    area_dropdown = craft_area_dropdown(page)
    office_dropdown = craft_office_dropdown(page)
    type_dropdown = craft_type_dropdown(page)
    reporttime_dropdown = craft_reporttime_dropdown(page)
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
                                type_dropdown,
                                reporttime_dropdown,
                            ],
                            scroll=True,
                        ),
                        ft.Text(return_text_data, size=30 ,weight="bold"),
                    ],
                    scroll=True,
                ),
            ],
            scroll=True,
        ),
    )

ft.app(target=main)