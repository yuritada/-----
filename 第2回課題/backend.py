import requests
import json

area_data = {}
response_data = {}

with open("area.json","r", encoding="utf-8") as f:
    area_data = json.load(f)

def reload():
    global response_data
    with open("response.json","r", encoding="utf-8") as f:
        response_data = json.load(f)

def zen_to_han(text):
    return text.translate(str.maketrans(
        "０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ．",
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz."
    ))




class back:
    def __init__(self, area_path: str, response_path: str):
        self.area_path = area_path
        self.response_path = response_path

    def load_area_codes(self):
        area_codes = {}
        for key, value in area_data["centers"].items():
            area_codes[key] = value["name"]
        return area_codes
    
    def load_office_codes(self, area_code: int):
        office_codes = area_data["centers"][area_code]["children"]
        office_list = {}
        for i in range(len(office_codes)):
            office_name = (area_data["offices"][office_codes[i]]["name"])
            office_list[office_codes[i]] = office_name
        return office_list

    def fetch_weather_data(self, office_code : int):
        request_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{office_code}.json"
        response = requests.get(request_url)
        if response.status_code == 200:
            data = response.json()
            with open(self.response_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return data

    def format_data_days(self):
        reload()
        weather_info = {}
        return_date = {}
        Number = 0
        for l in range(len(response_data)):
            for k in range(len(response_data[l]["timeSeries"])):
                for j in range(len(response_data[l]["timeSeries"][k]["areas"])):
                    for i in range(len(response_data[l]["timeSeries"][k]["timeDefines"])):
                        try:
                            # タイムスタンプの処理
                            raw_time = response_data[l]["timeSeries"][k]["timeDefines"][i].replace("T", "_").replace("+", ";")
                            full_time, _ = raw_time.split(";")
                            day, time = full_time.split("_")
                        except Exception as e:
                            print(f"Error1 processing time for area {j}, time {i}: {e}")
                            continue

                        weather_info = {}

                        # 日付と時間を追加
                        weather_info["day"] = day
                        weather_info["Time"] = time

                        # 地域名を取得
                        try :
                            area_name = response_data[l]["timeSeries"][k]["areas"][j].get("area", {}).get("name", "")
                            if area_name:
                                weather_info["area_name"] = area_name.replace("\u3000", " ")
                        except Exception as e:
                            pass
                        
                        # 天気コードを取得
                        try:
                            weather_code = response_data[l]["timeSeries"][k]["areas"][j].get("weatherCodes", [None])[i]
                            if weather_code:
                                weather_info["weather_code"] = weather_code.replace("\u3000", " ")
                        except Exception as e:
                            pass

                        # 天気名を取得
                        try:
                            weather_name = response_data[l]["timeSeries"][k]["areas"][j].get("weathers", [None])[i]
                            if weather_name:
                                weather_info["weather_name"] = weather_name.replace("\u3000", " ")
                        except Exception as e:
                            pass

                        # 風を取得
                        try:
                            wind = response_data[l]["timeSeries"][k]["areas"][j].get("winds", [None])[i]
                            if wind:
                                weather_info["wind"] = wind.split("\u3000")[0]
                        except Exception as e:  
                            pass

                        # 波を取得
                        try:
                            wave = response_data[l]["timeSeries"][k]["areas"][j].get("waves", [None])[i]
                            if wave:
                                weather_info["wave"] = zen_to_han(wave.replace("\u3000", " "))
                        except Exception as e:
                            pass 

                        try:
                            pops = response_data[l]["timeSeries"][k]["areas"][j].get("pops", [None])[i]
                            if pops:
                                weather_info["pops"] = pops
                        except Exception as e:
                            pass

                        try:
                            temps = response_data[l]["timeSeries"][k]["areas"][j].get("temps", [None])[i]
                            if temps:
                                weather_info["temps"] = temps
                        except Exception as e:
                            pass

                        try:
                            temps_Min = response_data[l]["timeSeries"][k]["areas"][j].get("tempsMin", [None])[i]
                            if temps_Min:
                                weather_info["temps_Min"] = temps_Min
                        except Exception as e:
                            pass

                        try:
                            temps_Max = response_data[l]["timeSeries"][k]["areas"][j].get("tempsMax", [None])[i]
                            if temps_Max:
                                weather_info["temps_Max"] = temps_Max
                        except Exception as e:
                            pass
                        # 完成したデータを追加
                        print(weather_info)
                        return_date[f"{Number}"] = weather_info
                        Number += 1



                    Number = j * 100 + 100
            
        with open("workbench.json", 'w', encoding='utf-8') as f:
            json.dump(return_date, f, ensure_ascii=False, indent=4)

        return return_date

        
if __name__ == "__main__":
    reload()
    # JSONファイルのパス
    area_path = "area.json"
    response_path = "response.json"
    area_code = "140000"  # サンプル地域コード

    # クラスのインスタンス化
    お試しオブジェクト = back(area_path, response_path)

    # 地域コード一覧の取得
    areas = お試しオブジェクト.load_area_codes()

    # 天気データの取得と保存
    weather_data = お試しオブジェクト.fetch_weather_data(area_code)

    # 天気データの整形
    parsed_data = お試しオブジェクト.format_data_days()
    print("整形された天気データ:", parsed_data )

