from aiogram import Bot,Dispatcher
from .jsn_function.read_json import read_json

data = read_json(name_json = "config_api.json")

TOKEN = data["api_key_tg"]
dp = Dispatcher()
bot = Bot(TOKEN)