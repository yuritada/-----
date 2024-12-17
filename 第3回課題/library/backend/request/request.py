import requests
import json

def request_weather_data(office_code):
    request_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{office_code}.json"
    response = requests.get(request_url)
    if response.status_code == 200:
        return office_code , response.json()
    else:
        print(f"Failed to fetch weather data for {office_code}")

if __name__ == "__main__":
    print(request_weather_data("015000"))