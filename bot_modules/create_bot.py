from aiogram import Bot, Dispatcher, Router
from .json_function.read_json import read_json

# Создаём объект класса роутер
router = Router()

data = read_json(name_json = "config_api.json")

TOKEN = data["api_key_tg"]
dp = Dispatcher()
bot = Bot(TOKEN)