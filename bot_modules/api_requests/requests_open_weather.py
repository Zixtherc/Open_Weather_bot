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


import requests
import json

def request_city_user(city_name: str, count: int = 0):
    # Запрос к API OpenWeather
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric&lang=uk&cnt=4"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Десериализация ответа JSON
        weather_data = json.loads(response.content)

        # Загружаем данные в JSON файл (предполагается, что у вас есть функция load_json)
        load_json(name_json="load_weather.json", value_file=weather_data)

        try:
            # Пробуем получить данные для текущего индекса
            current = weather_data["list"][count]

            # Извлекаем информацию о погоде
            temperature_celsius = round(current["main"]["temp"])
            humidity = current["main"]["humidity"]
            visibility = current.get("visibility", "Нет данных") 
            wind = current["wind"]["speed"]
            user_city_name = weather_data["city"]["name"]

            return temperature_celsius, humidity, visibility, wind, user_city_name
        except IndexError:
            # Если индекс выходит за пределы доступных данных
            return None
    else:
        # Если запрос не удался, возвращаем код ошибки
        error = response.status_code
        print(f"Ошибка при запросе: {error}")
        return error
