import json
import csv
import requests

json_path = '第二回課題/area.json'
response_path = '第二回課題/response.json'
area_code = '011000'
request_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
csv_file_path = "第二回課題/response.csv"

# jsonファイルの読み込み
with open(json_path) as f:
    area = json.load(f)

response = requests.get(request_url)

# jsonファイルの書き込み、ファイルがある場合は上書き、文字コードはutf-8
with open(response_path, 'w', encoding='utf-8') as f:
    json.dump(response.json(), f, ensure_ascii=False, indent=4)


