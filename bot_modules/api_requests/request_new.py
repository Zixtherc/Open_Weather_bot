import requests
import json

from ..jsn_function.read_json import read_json
from ..jsn_function.load_json import load_json



api_dict = read_json(name_json = "config_api.json")

API_KEY = api_dict["api_key_news"]


def request_news(country: str = "USA", count : int = 0, flag_country : bool = False):

    if flag_country:
        print(f'Зашло ')
        URL = f"https://newsapi.org/v2/top-headlines?q={country}&apiKey={API_KEY}"

        response = requests.get(URL)
        if response.status_code == 200:

            news_data = json.loads(response.content)
            load_json(name_json="load_news.json", value_file=news_data)
            news_id = news_data["articles"][count]

            news_author = news_id["author"]
            news_title = news_id["title"]
            news_description = news_id["description"]
            news_source = news_id["url"]
            news_time = news_id["publishedAt"]

            return news_author, news_title, news_description, news_source, news_time

        else:
            print(f'Неудачная попытка реквеста')
    else:
        URL = f"https://newsapi.org/v2/top-headlines?sources=bbc-news,cnn&apiKey={API_KEY}"

        response = requests.get(URL)

        if response.status_code == 200:
            news_data = json.loads(response.content)
            load_json(name_json="load_news.json", value_file=news_data)
            current = news_data["articles"][count]["source"]["id"]
            print(current)
        else:
            print(f'Неудачная попытка реквеста')


request_news(count = 0, flag_country = True)