from aiogram.types import Message
from .create_bot import dp
from aiogram.filters import CommandStart, Command
from .api_requests.requests_open_weather import request_city_user
from .api_requests.requests_caledarfic import request_holiday

        
@dp.message(CommandStart())
async def start (message : Message):
    await message.answer("Hello !")

@dp.message(Command("weather"))
async def request_weather(message: Message):
    await message.answer("Enter city name ( only in English )")

@dp.message()
async def city_wait(message : Message):
    city_user = message.text.strip()
    print(city_user)
    
    if city_user:
        weather_info = request_city_user(city_user)

        if request_city_user(city_name = city_user):
            if weather_info:
                temperature_celsius, humidity, visibility, wind, user_city_name = weather_info
                response_text = (f"Погода в {user_city_name}:\n"
                                f"Температура: {temperature_celsius}°C\n"
                                f"Влажность: {humidity}%\n"
                                f"Видимость: {visibility} м\n"
                                f"Скорость ветра: {wind} м/c")
                await message.reply(response_text)

        else:
            await message.reply("Try again") 

    else:
        await message.reply("Try again")


@dp.message(Command("holidays_tg_hz"))
async def com_request_holidays(message : Message):
    await message.answer("Enter country name, and year")
  
@dp.message()
async def holidays_wait(message : Message):
    user_text_non_split = message.text
    user_country , user_year = user_text_non_split.split()
    print(user_country)
    print(user_year)
    
    if user_country and user_year:
        holidays_info = request_holiday(country_name = user_country, year = int)
        if holidays_info:
            print(holidays_info)