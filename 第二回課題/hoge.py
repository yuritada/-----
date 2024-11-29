import json

json_path = '第二回課題/response.json'

with open(json_path) as f:
    area = json.load(f)

print(area[0]["timeSeries"][0]["areas"][0]["weathers"][1])