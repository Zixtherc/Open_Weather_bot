# Необходимые импорты
from aiogram import Router
from aiogram.types import Message
from .create_bot import dp
from aiogram.filters import CommandStart, Command
# Импорты функций
from .api_requests.requests_open_weather import request_city_user
from .api_requests.requests_caledarfic import request_holiday
# Импорт состояний для управления вводом пользователя
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# Создаём класс роутера 
router = Router()

# Создаём класс для управления вводом пользователя 
class Form(StatesGroup):
    waiting_for_city = State()
    holiday = State()

# Создаём реагирование на команду /start
@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello!")

# Создаём реагирование на команду /weather
@router.message(Command("weather"))
async def request_weather(message: Message, state: FSMContext):
    await message.answer("Enter city name (only in English)")
    # Устанавливаем состояние ожидание ввода города
    await state.set_state(Form.waiting_for_city)

# Если состояние "ожидание города" активно , вызывается эта функция
@router.message(Form.waiting_for_city)
async def city_wait(message: Message, state: FSMContext):

    # Очищаем текст пользователя от лишних пробелов и т.д
    city_user = message.text.strip()
    print(city_user)

    # Проверяем есть ли в переменной какие-то значения, если да , то она True, если нет, то False

    if city_user:
        # записываем в переменную weather_info всю информации функции которая отработает

        weather_info = request_city_user(city_user)
        # Проверяем есть ли в этой функции какие-то значения

        if weather_info:

            # Создаём переменные, и берём из переменной weather_info, всю не обходимую информацию
            temperature_celsius, humidity, visibility, wind, user_city_name = weather_info
            # Записываем в другую перемнную всю информацию для более удобного вывода
            response_text = (f"Погода в {user_city_name}:\n"
                             f"Температура: {temperature_celsius}°C\n"
                             f"Влажность: {humidity}%\n"
                             f"Видимость: {visibility} м\n"
                             f"Скорость ветра: {wind} м/c")
            # Выводим текст
            await message.reply(response_text)
            # Очищаем состояние
            await state.clear()
        # Иначе выводим текст     
        else:
            await message.reply("Try again")
    else:
        await message.reply("Try again")

#Создаём  реагирование на команду /holidaysz
@router.message(Command("holidaysz"))
async def com_request_holidays(message: Message, state: FSMContext):
    await message.answer("Enter country name and year")
    # Устанавливаем состояние в ожидании ответа пользователя  
    await state.set_state(Form.holiday)

#Если состояние "ожидание праздинка"активно , вызывается эта функция 
@router.message(Form.holiday)
async def process_holiday(message: Message, state: FSMContext):
    # Очищаем текст пользователя от лишних пробелов
    user_input = message.text.strip()

    # Пытаемся разделить текст пользователя по пробелу, чтобы получить страну и год
    country_year = user_input.split()
    if len(country_year) == 2:
        country, year = country_year
        print(country, "\n", year)

        # Обновляем состояние, где country — переменная страны, а year — переменная года
        await state.update_data(country=country, year=year)

        # Выводим, что ввёл пользователь
        await message.reply(f"Country: {country}, Year: {year}")

        # Запрашиваем данные о праздниках
        try:
            holidays_data = request_holiday(country_name=country, year=year)

            if holidays_data:
                holidays, country, year = holidays_data
                response_text = f"Holidays: {holidays}, Country: {country}, Year: {year}"
                await message.reply(response_text)
            else:
                await message.reply("No holiday data found for the specified country and year.")
        except Exception as e:
            await message.reply("An error occurred while fetching holiday data.")
            print(f"Error fetching holiday data: {e}")
    else:
        await message.reply("Invalid format. Please enter 'country year'.")

    # Очищаем состояние после обработки
    await state.clear()