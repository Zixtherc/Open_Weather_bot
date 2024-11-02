# Импорты 
import requests
import json
# Импортируем функцию, которая позволит нам читать json файлы
from ..jsn_function.read_json import read_json
from ..jsn_function.load_json import load_json

# Читаем json файл, и записываем в переменную (чтобы каждый раз не вызывать функцию)
api_dict = read_json(name_json="config_api.json")

#записываем API ключ
API_KEY = api_dict["api_key"]


def request_city_user(city_name : str):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
    response = requests.post(url, city_name)
    
  
    if response.status_code == 200:
      
      weather_data = json.loads(response.content)
      load_json(name_json = "load_files.json", value_file = weather_data)
      print(json.dumps(weather_data, indent = 4))

      temperature_kelvin = round(weather_data["main"]["temp"])
      temperature_celsius = round(temperature_kelvin - 273.15)
      humidity = round(weather_data["main"]["humidity"])
      visibility = round(weather_data["visibility"])
      wind = round(weather_data["wind"]["speed"])
      user_city_name = weather_data["name"]
      # rain = weather_data["rain"]["1h"]
      # clouds = round(weather_data["clouds"])
      
      return temperature_celsius, humidity, visibility, wind, user_city_name


    else:
      error = response.status_code
      print(response.status_code)
      return error