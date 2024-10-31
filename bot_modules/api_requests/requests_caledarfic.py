import json
import requests
from ..jsn_function.load_json import load_json
from ..jsn_function.read_json import read_json

api_dict_holiday = read_json(name_json = "config_api.json")
API_KEY_HOLIDAY = api_dict_holiday["api_key_holidays"]

def request_holiday(country_name : str, year : int):

    url = f"https://calendarific.com/api/v2/holidays?api_key={API_KEY_HOLIDAY}&country={country_name}&year={year}"
    response = requests.post(url)
    if response.status_code == 200:

        holidays_data = json.loads(response.content)
        load_json (name_json = "load_holidays.json" , value_file = holidays_data)
        print(json.dumps(holidays_data, indent = 4))