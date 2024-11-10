import json
import requests

# Импорты функций
from ..jsn_function.read_json import read_json
from ..jsn_function.load_json import load_json

# Читаем словарь при помощи функции
api_dict_holiday = read_json(name_json = "config_api.json")
# Получаем API ключ из словаря
API_KEY_HOLIDAY = api_dict_holiday["api_key_holidays"]


# Создаём функцию для запроса на праздники
def request_holiday(country_code: str, year: int):
    # Параметры запроса
    params = {
        'key': API_KEY_HOLIDAY,
        'country': country_code,
        'year': year
    }

    # Формируем URL для запроса
    url = "https://holidayapi.com/v1/holidays"

    # Отправляем запрос с параметрами
    response = requests.get(url, params=params)

    # Проверяем статус ответа
    if response.status_code == 200:
        # Парсим данные из ответа
        holidays_data = response.json()
        # Сохраняем данные в файл (если эта функция есть)
        load_json(name_json="load_holidays.json", value_file=holidays_data)
        # Выводим информацию для отладки
        # print(json.dumps(holidays_data, indent=4))
        print("URL запроса:", response.url)
        
        return holidays_data
        
    else:
        print(response.url)
        # Если запрос не успешен, выводим ошибку
        print(f"Ошибка при запросе, код: {response.status_code}")
        print("Полный ответ:", response.text)

        return response.status_code