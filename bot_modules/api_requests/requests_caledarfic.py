# Необходимые импорты
import json
import requests

# Импорты функций
from ..jsn_function.read_json import read_json
from ..jsn_function.load_json import load_json

# Читаем словарь при помощи функции
api_dict_holiday = read_json(name_json = "config_api.json")
# Получаем API ключ из словаря
API_KEY_HOLIDAY = api_dict_holiday["api_key_holidays"]

# Создаём функция для запроса на праздники
def request_holiday(country_name : str, year : int):
    # Записываем в переменную url адрес куда мы будем отсылать запросы 
    url = f"https://calendarific.com/api/v2/holidays?api_key={API_KEY_HOLIDAY}&country={country_name}&year={year}"

    # Создаём запрос
    response = requests.post(url)
    #Проверяем статус запроса ( 200 - успешный )
    if response.status_code == 200:

        # Записываем в переменную весь "контент" запроса 
        holidays_data = json.loads(response.content)
        # Cохраняем контент в файле json
        load_json(name_json = "load_holidays.json", value_file=holidays_data)
        # Выводим текст 
        print (json.dumps(holidays_data, indent=4))
        # Записываем в переменную нужную для нас информацию
        holidays = holidays_data.get("response", {}).get("holidays", [])
        # Возвращаем всё что нам надо
        return holidays, country_name, year
    
    else:
        # Записываем в переменную статус ошибки
        error = response.status_code
        # Возвращаем код ошибки
        return error