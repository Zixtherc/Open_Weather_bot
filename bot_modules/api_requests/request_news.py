'''
:mod:`Модуль`, который позволит отправлять :mod:`Запросы` на бесплатное :mod:`API`, сайта :mod:`NEWSAPI`
'''
# Необходимый модуль для отправки запросов
import requests
# Модуль json,нужен для преобразования данных 
import json
# Необходимые модули что бы прочитать и записать данные из json файла / в json файл
from ..json_function.read_json import read_json
from ..json_function.load_json import load_json

# Импортируем функцию, для перевода текста (пока в разработке)
from ..useful_func.google_trans import my_translate
# Читаем все данные из json файла
api_dict = read_json(name_json = "config_api.json")

# Записываем ключ API в переменную
API_KEY = api_dict["api_key_news"]


def request_news(country: str, count : int = 0, language : str = "ru"):
    r'''
    Создаём функцию с параметрами :
    - :mod:`country`: `параметр` для отправки запроса по `указанной` стране пользователя
    - :mod:`count`: `параметр` для указания `порядкового` `номера` новости, которую необходимо получить (по умолчанию 0)
    '''
    # Создаём проверку что пользователь ввёл какую-либо информацию 
    if country:
        # Формируем URL для запроса
        URL = f"https://newsapi.org/v2/top-headlines?q={country}&apiKey={API_KEY}"

        # Записываем в переменную response, ответ который мы получили по указанном URL
        response = requests.get(URL)

        # Проверяем что запрос успешно выполнен
        if response.status_code == 200:
            try:
                # Десериализация ответа JSON
                news_data = json.loads(response.content)
                # Загружаем данные в JSON файл (предполагается, что у вас есть функция load_json)
                load_json(name_json="load_news.json", value_file=news_data)
                # Создаём переменную для упрощения кода, к параметру count
                news_id = news_data["articles"][count]

                # Создаём переменную в которой хранится автор статьи
                news_author = my_translate(text = news_id["author"], lang = language)
                # Создаём переменную в которой хранится заголовок статьи
                news_title = my_translate(text = news_id["title"], lang = language)
                # Создаём переменную в которой хранится описание статьи
                news_description = my_translate(text = news_id["description"], lang = language)
                # Создаём переменную в которой хранится ссылка на источник статьи
                news_source = news_id["url"]
                # Создаём переменную в которой хранится дата публикации статьи
                news_time = my_translate(text = news_id["publishedAt"])
                # Преобразуем дату из формата ISO 8601 в формат dd.mm.yyyy
                ready_time = news_time.split("T")[0]
                len_count_news = len(news_data["articles"])
                # Возвращаем нужные нам данные
                return news_author, news_title, news_description, news_source, ready_time, len_count_news
            except IndexError as e:
                return None

        # Если ответ не успешный
        else:
            print(f'Неудачная попытка реквеста')
            return
    # Если пользователь не ввёл коректные данные, отправляем ему данные с источника bbc
    else:
        
        # Формируем URL для запроса
        URL = f"https://newsapi.org/v2/top-headlines?sources=bbc-news,cnn&apiKey={API_KEY}"

        # Записываем в переменную response, ответ который мы получили по указанном URL
        response = requests.get(URL)
        # Проверяем что запрос успешно выполнен
        if response.status_code == 200:
            try:
                # Десериализация ответа JSON
                news_data = json.loads(response.content)
                # Загружаем данные в JSON файл (предполагается, что у вас есть функция load_json)
                load_json(name_json="load_news.json", value_file=news_data)
                # Создаём переменную для упрощения кода, к параметру count, добавляем по +1, так-как в новость идёт с нуля
                news_id = news_data["articles"][count]
                # Создаём переменную в которой хранится автор статьи
                news_author = my_translate(text = news_id["author"], lang = language)
                # Создаём переменную в которой хранится заголовок статьи
                news_title = my_translate(text = news_id["title"], lang = language)
                # Создаём переменную в которой хранится описание статьи
                news_description = my_translate(text = news_id["description"], lang = language)
                # Создаём переменную в которой хранится ссылка на источник статьи
                news_source = news_id["url"]
                # Создаём переменную в которой хранится дата публикации статьи
                news_time = news_id["publishedAt"]
                # Преобразуем дату из формата ISO 8601 в формат dd.mm.yyyy
                ready_time = news_time.split("T")[0]
                len_count_news = len(news_data["articles"])
                # Возвращаем нужные нам данные
                return news_author, news_title, news_description, news_source, ready_time, len_count_news
            except IndexError as error:
                return None
        else:
            print(f'Неудачная попытка реквеста')
            return