import requests
import json

from ..jsn_function.read_json import read_json
from ..jsn_function.load_json import load_json

from os.path import abspath, join
import json

def load_json(name_json : str, value_file : str):
    path = abspath(join(__file__, '..', '..', 'static', name_json))
    
    with open (file = path, mode = "w", encoding = "utf-8") as file:
        json.dump(
            obj = value_file,
            ensure_ascii = False,
            indent = 4,
            fp = file
        )
api_dict = read_json(name_json = "config.json")

API_KEY = api_dict["api_key_news"]


def request_news(country: str = "ua"):
    URL = f"https://newsapi.org/v2/top-headlines?sources=bbc-news,cnn&apiKey={API_KEY}"

    response = requests.get(URL)

    if response.status_code == 200:
        news_data = json.loads(response.content)
        load_json(name_json="load_news.json", value_file=news_data)
        current = news_data["articles"][0]["source"]["id"]
        print(current)
    else:
        print(f'Неудачная попытка реквеста, соси член')


request_news(country= "ua")