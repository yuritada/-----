import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
from library.backend.request.request import request_weather_data

def adjust_weather_data_for_weather_day_table(office_code,response):
    return_data = []
    for i in range(len(response[0]["timeSeries"][0]["timeDefines"])):
        for j in range(len(response[0]["timeSeries"][0]["areas"])):
            data = {}
            data["office_code"] = office_code
            data["area_name"] = response[0]["timeSeries"][0]["areas"][j]["area"]["name"]
            data["report_datetime"] = response[0]["reportDatetime"]
            data["time_defines"] = response[0]["timeSeries"][0]["timeDefines"][i]
            data["weather_code"] = response[0]["timeSeries"][0]["areas"][j]["weatherCodes"][i]
            data["weather_name"] = response[0]["timeSeries"][0]["areas"][j]["weathers"][i]
            data["wind"] = response[0]["timeSeries"][0]["areas"][j]["winds"][i]
            try:
                data["wave"] = response[0]["timeSeries"][0]["areas"][j]["waves"][i]
            except:
                data["wave"] = None
            return_data.append(data)
    return return_data

def adjust_weather_data_for_weather_day_pops_table(office_code,response):
    return_data = []
    for i in range(len(response[0]["timeSeries"][1]["timeDefines"])):
        for j in range(len(response[0]["timeSeries"][1]["areas"])):
            data = {}
            data["office_code"] = office_code
            data["area_name"] = response[0]["timeSeries"][1]["areas"][j]["area"]["name"]
            data["report_datetime"] = response[0]["reportDatetime"]
            data["time_defines"] = response[0]["timeSeries"][1]["timeDefines"][i]
            data["pops"] = response[0]["timeSeries"][1]["areas"][j]["pops"][i]
            return_data.append(data)
    return return_data

def adjust_weather_data_for_weather_day_temps_table(office_code,response):
    return_data = []
    for i in range(len(response[0]["timeSeries"][2]["timeDefines"])):
        for j in range(len(response[0]["timeSeries"][2]["areas"])):
            data = {}
            data["office_code"] = office_code
            data["area_name"] = response[0]["timeSeries"][2]["areas"][j]["area"]["name"]
            data["report_datetime"] = response[0]["reportDatetime"]
            data["time_defines"] = response[0]["timeSeries"][2]["timeDefines"][i]
            data["temps"] = response[0]["timeSeries"][2]["areas"][j]["temps"][i]
            return_data.append(data)
    return return_data

if __name__ == "__main__":
    code , response = request_weather_data("015000")
    print(adjust_weather_data_for_weather_day_table(code,response))
    print(adjust_weather_data_for_weather_day_pops_table(code,response))
    print(adjust_weather_data_for_weather_day_temps_table(code,response))