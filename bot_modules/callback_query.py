from aiogram.types import Message
from .create_bot import dp
from aiogram.filters import CommandStart, Command
from .api_requests.requests_open_weather import request_city_user

        
@dp.message(CommandStart())
async def start (message : Message):
    await message.answer("Hello !")

@dp.message(Command("weather"))
async def request (message: Message):
    await message.answer("Enter city name ( only in English )")

@dp.message()
async def city_wait(message : Message):
    city_user = message.text.strip()
    print(city_user)
    
    if city_user:
        weather_info = request_city_user(city_user)

        if request_city_user(city_name = city_user):
            if weather_info:
                temperature_celsius, humidity, visibility, wind = weather_info
                response_text = (f"Погода в {city_user.capitalize()}:\n"
                             f"Температура: {temperature_celsius}°C\n"
                             f"Влажность: {humidity}%\n"
                             f"Видимость: {visibility} м\n"
                             f"Скорость ветра: {wind} м/c")

        else:
            await message.reply("Try again") 

    else:
        await message.reply("Try again")