import json
import requests

class WeatherAPI:
    def __init__(self, json_path: str, response_path: str):
        self.json_path = json_path
        self.response_path = response_path

    def load_area_codes(self):
        """地域コードを取得する"""
        with open(self.json_path, encoding="utf-8") as f:
            area_data = json.load(f)
        return area_data["offices"]

    def fetch_weather_data(self, area_code: str):
        """指定された地域コードでAPIから天気データを取得する"""
        request_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
        response = requests.get(request_url)
        if response.status_code == 200:
            data = response.json()
            with open(self.response_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return data
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    def load_weather_data(self):
        """ローカルに保存された天気データをロードする"""
        with open(self.response_path, encoding="utf-8") as f:
            return json.load(f)

    def parse_weather_data(self, data, area_code):
        """APIから取得したデータをパースして整形する"""
        for entry in data:
            for area in entry["timeSeries"][0]["areas"]:
                if area["area"]["code"] == area_code:
                    weather_info = {
                        "publishingOffice": entry["publishingOffice"],
                        "reportDatetime": entry["reportDatetime"],
                        "weather": area["weathers"],
                        "wind": area["winds"],
                        "wave": area["waves"],
                    }
                    return weather_info
        raise ValueError("Area code not found in data.")
    
if __name__ == "__main__":
    # JSONファイルのパス
    json_path = "area.json"
    response_path = "response.json"
    area_code = "011000"  # サンプル地域コード

    # クラスのインスタンス化
    weather_api = WeatherAPI(json_path, response_path)

    # 地域コード一覧の取得
    areas = weather_api.load_area_codes()
    print("地域コード一覧:", areas)

    # 天気データの取得と保存
    weather_data = weather_api.fetch_weather_data(area_code)

    # 保存済みデータのロード
    saved_data = weather_api.load_weather_data()

    # 天気データの整形
    parsed_data = weather_api.parse_weather_data(saved_data, area_code)
    print("整形された天気データ:", parsed_data)