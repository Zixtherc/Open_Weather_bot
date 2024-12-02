# Необходимые импорты
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from .create_bot import dp
from aiogram.filters import CommandStart, Command

# Импорты функций
from .api_requests.requests_open_weather import request_city_user
#                from .api_requests.requests_caledarfic import request_holiday

# Импорты клавиатур 
from .keyboard.keyboard import inline_keyboard, forecast_keyboard

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
    await message.answer("Hello!", reply_markup = inline_keyboard)

# Создаём обработчик на коллбек weather
@router.callback_query(F.data == "weather")
async def request_weather(callback : CallbackQuery, state: FSMContext):

    await callback.answer('')   
    await callback.message.answer("Enter city name")
    # Устанавливаем состояние ожидание ввода города
    await state.set_state(Form.waiting_for_city)

# Если состояние "ожидание города" активно , вызывается эта функция
@router.message(Form.waiting_for_city)
async def city_wait(message: Message, state: FSMContext):
    
    # Очищаем текст пользователя от лишних пробелов и т.д
    city_user = message.text.strip()

    # Проверяем есть ли в переменной какие-то значения
    if city_user:
    
        # Получаем данные для города с учетом текущего значения count
        weather_info = request_city_user(city_user, count = 0)

        # Если данные найдены
        if weather_info:

            # Создаём переменные, и берём из переменной weather_info, всю не обходимую информацию
            temperature_celsius, humidity, visibility, wind, user_city_name = weather_info

            # Формируем текст прогноза для текущего периода и добавляем в общий текст
            response = (f"Погода в {user_city_name}:\n"
                        f"Температура: {temperature_celsius}°C\n"
                        f"Влажность: {humidity}%\n"
                        f"Видимость: {visibility} м\n"
                        f"Скорость ветра: {wind} м/c\n\n")
            # Обновляем состояние city_user и coutn 
            await state.update_data(city_user=city_user, count=0)
        
        # Если данные не найдены, то  Выводим ошибку
        else:
            await message.reply("Ошибка с запросом")
            

        # Если есть прогнозы, отправляем их все в одном сообщении
        if response:
            await message.reply(response, reply_markup = forecast_keyboard)

        # Если нет, то выводим ошибку
        else:
            await message.reply("Не удалось найти данные для города.")
    # Если нет, то выводим ошибку
    else:
        await message.reply("Попробуйте снова.")

# Создаём обработчик на коллбек next
@router.callback_query(F.data == "next")
async def n_forecast(callback: CallbackQuery, state: FSMContext):

# Получаем все состояния 
    data = await state.get_data()
    # Записываем в переменную состояние count
    count = data.get("count", 0) + 1

    # Проверяем, чтобы count не стал меньше 0
    if count >= 4:
        await callback.answer("Вы достигли минимального значения прогноза.", show_alert=True)
        
        return  # Прерываем выполнение функции

    # Записываем в переменную состояние city_user
    city_user = data.get("city_user")
    
    # Получаем данные из функции отправки запросов 
    weather_info = request_city_user(city_name=city_user, count=count)
    
    # Проверяем есть ли в weather_info какие-либо значения
    if weather_info:

        # Создаём переменные для удобного вывода
        temperature_celsius, humidity, visibility, wind, user_city_name = weather_info

        # Группируем переменные в одну
        forecast = (f"Погода в {user_city_name}:\n"
                    f"Температура: {temperature_celsius}°C\n"
                    f"Влажность: {humidity}%\n"
                    f"Видимость: {visibility} м\n"
                    f"Скорость ветра: {wind} м/c\n\n")
        
        # Обновляем состояние количества 
        await state.update_data(count=count)
        # Редактируем текст с клавиатурой
        await callback.message.edit_text(forecast, reply_markup=forecast_keyboard)
    # Если данных нет, то выводим ошибку
    else:
        await callback.message.edit_text("Не удалось получить данные о погоде.")

# Создаём обработчик на коллбек back
@router.callback_query(F.data == "back")
async def b_forecast(callback: CallbackQuery, state: FSMContext):

    # Получаем все состояния 
    data = await state.get_data()
    # Записываем в переменную состояние count
    count = data.get("count", 0) - 1

    # Проверяем, чтобы count не стал меньше 0
    if count < 0:
        await callback.answer("Вы достигли минимального значения прогноза.", show_alert=True)
        return  # Прерываем выполнение функции

    # Записываем в переменную состояние city_user
    city_user = data.get("city_user")
    
    # Получаем данные из функции отправки запросов 
    weather_info = request_city_user(city_name=city_user, count=count)
    
    # Проверяем есть ли в weather_info какие-либо значения
    if weather_info:

        # Создаём переменные для удобного вывода
        temperature_celsius, humidity, visibility, wind, user_city_name = weather_info

        # Группируем переменные в одну
        forecast = (f"Погода в {user_city_name}:\n"
                    f"Температура: {temperature_celsius}°C\n"
                    f"Влажность: {humidity}%\n"
                    f"Видимость: {visibility} м\n"
                    f"Скорость ветра: {wind} м/c\n\n")
        
        # Обновляем состояние количества 
        await state.update_data(count=count)
        # Редактируем текст с клавиатурой
        await callback.message.edit_text(forecast, reply_markup=forecast_keyboard)
    # Если данных нет, то выводим ошибку
    else:
        await callback.message.edit_text("Не удалось получить данные о погоде.")