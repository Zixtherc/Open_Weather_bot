# Необходимые импорты
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

# Импорт для красивого вывода в терминал (необязательно)
import colorama

# Импорты функций
from .api_requests.requests_open_weather import request_city_user
from .useful_func.scheduled_messages import schedule
from .api_requests.request_news import request_news

# Импорты клавиатур 
from .keyboard.keyboard import inline_keyboard, forecast_keyboard, news_keyboard

# Импорт состояний для управления вводом пользователя
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext



# Создаём объект класса роутер
router = Router()

# Создаём класс для управления вводом пользователя 
class Form(StatesGroup):
    waiting_for_city = State()
    holiday = State()
    wait_data_diary = State()
    wait_data_news = State()

# Создаём реагирование на команду /start
@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello!", reply_markup = inline_keyboard)

# Создаём обработчик на команду /help
@router.message(Command("help"))
async def send_commands(message: Message):
    await message.answer(
        "Здравствуйте, вот список всех доступных команд на данный момент:\n"
        "/weather - Получить прогноз погоды\n"
        "/diary - Создать запланирование сообщение\n"
        "/news - Получить последние новости"
    )
# Создаём обработчик на коллбек weather
@router.callback_query(F.data == "weather")
async def request_weather(callback : CallbackQuery, state: FSMContext):
    await callback.answer('')   
    await callback.message.answer("Enter city name")
    # Устанавливаем состояние ожидание ввода города
    await state.set_state(Form.waiting_for_city)

@router.message(Command("weather"))
async def request_weather(message : Message, state: FSMContext):
    await message.answer("Введите название города. Пример : `Киев`")
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
            
            try:
                # Создаём переменные, и берём из переменной weather_info, всю не обходимую информацию
                temperature_celsius, humidity, visibility, wind, user_city_name = weather_info

                # Формируем текст прогноза для текущего периода и добавляем в общий текст
                response = (f"Погода в {user_city_name}:\n"
                            f"Температура: {temperature_celsius}°C\n"
                            f"Влажность: {humidity}%\n"
                            f"Видимость: {visibility} м\n"
                            f"Скорость ветра: {wind} м/c\n\n")
                # Обновляем состояние city_user и count
                await state.update_data(city_user=city_user, count=0)
            except Exception as error:
                await message.reply(f"К сожалению, вы не правильно ввели данные,попробуйте проверить и ввести всё верно. Код ошибки: {error}")
        
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

# Создаём обработчик на callback diary
@router.callback_query(F.data == "diary")
async def wait_data_diary(callback : CallbackQuery, state : FSMContext):
    callback.message.answer(' ')
    await callback.message.answer("Введите время запланированого сообщения и его текст МИНУТЫ,или ТОЧНУЮ ДАТУ отложенного сообщения,вместе с МИНУТАМИ")
    # Устанавливаем состояние
    await state.set_state(Form.wait_data_diary)

# Создаём обработчик на команду diary
@router.message(Command('diary'))
async def wait_data_diary(message : Message, state : FSMContext):
    await message.answer("Введите время запланированого сообщения и его текст МИНУТЫ,или ТОЧНУЮ ДАТУ отложенного сообщения,вместе с МИНУТАМИ")
    # Устанавливаем состояние
    await state.set_state(Form.wait_data_diary)

# Создаём обработчик если состояние есть
@router.message(Form.wait_data_diary)
# Функция для использования функции отложенных сообщений
async def schedule_send(message : Message, state : FSMContext):
    # Получаем id чата 
    chat_id = message.chat.id
    # Получаем данные из состояния
    data = await state.get_data()
    # Получаем текст определенные данные, и текст
    user_data = data.get('wait_data_diary', message.text)
    # Делим текст пользователя по пробелу, 1 раз
    ready_data = user_data.split(' ', 2)
    # Получаем время полученных данных
    time = f'{ready_data[0]}.{ready_data[1]}'
    print(f'Это время поаааааа{time}')
    # Получаем текст полученных данных
    text = ready_data[-1]

    # Используем операторы try, excep, для безопасного использования
    try:
        # Вызываем функцию отложенных сообщений, в параметр записываем выше указанные переменные
        await schedule(exact_date = time, chat_id = chat_id, message_text = text)
        # Выводим данные в терминал (не обязательно)
        print(f'{colorama.Fore.CYAN} Всё получилось, сообщение и функция отработала {colorama.Style.RESET_ALL}')
    # Обрабатываем ошибку, если она возникнет при вызове функции
    except Exception as error:
        await message.answer(f'Ошибка при создании отложенного сообщения. Ошибка : {error}')
        return

# Создаём обработчик на callback news
@router.callback_query(F.data == "news")
async def wait_data_news(callback: CallbackQuery, state: FSMContext):
    callback.message.answer(' ')
    await callback.message.answer("Введите страну по которой хотите получить новость")
    # Устанавливаем состояние
    await state.set_state(Form.wait_data_news)
    
# Создаём обработчик на команду news
@router.message(Command("news"))
async def wait_data_news(message: CallbackQuery, state: FSMContext):
    await message.answer("Введите страну по которой хотите получить новость")
    # Устанавливаем состояние
    await state.set_state(Form.wait_data_news)

# Создаём обработчик если состояние есть
@router.message(Form.wait_data_news)
async def send_news(message: Message, state: FSMContext):
    # Получаем все данные из состояний
    data = await state.get_data()
    # Получаем текст определенные данные, и текст
    user_data = data.get('wait_data_news', message.text)
    # Делим текст пользователя по пробелу
    ready_data = user_data.split(' ')
    # Записываем данные в переменную страны
    country = ready_data[0]
    # Какая новость по счету интересна пользователю
    count = 0
    # Используем операторы try, except, для безопасного использования
    try:
        # Если в переменной есть какие-то данные
        if country:
            # Вызываем фукнцию, и записываем данные в переменную
            news_info = request_news(country = country, count = count)
            # Если данные есть, и функция отработала
            if news_info:
                # Делим в каждую переменную данные который нам надо
                news_author, news_title, news_description, news_source, news_time, count_news = news_info

                # Группируем переменную для удобной отправки  
                news_message = (
                    f"Заголовок: {news_title}\n"
                    f"Автор: {news_author}\n"
                    f"Дата публікації: {news_time}\n"
                    f"Опис: {news_description}\n"
                    f"Джерело: {news_source}")
                
                await state.update_data(country = country, count_news = count_news)

                # Отправляем данные
                await message.answer(news_message, reply_markup = news_keyboard)
        # Если данных по указанной стране нету
        else:
            # Отправляем сообщение пользователю
            await message.answer("К сожалению по указанным данным нету новостей")
            return 
    # Обрабатываем ошибку, если она возникнет при вызове функции
    except Exception as error:
        # Выводим ошибку пользователю 
        await message.answer(f'Ошибка при запроса новостей, код ошибки : {error}')

@router.callback_query(F.data == "next_news")
async def n_news(callback : CallbackQuery, state : FSMContext):
    data = await state.get_data()
    count_news = data.get('count_news', 0) + 1
    print(count_news)
    count = 0
    if count >= count_news:
        await callback.answer('Вы достигли максимального значения новостей', show_alert = True)
        return
    country = data.get("country")
    news_info = request_news(country = country, count = count)
    count += 1 
    if news_info:
        news_author, news_title, news_description, news_source, news_time, count_news = news_info
        # Группируем переменную для удобной отправки  
        news_message = (
            f"Заголовок: {news_title}\n"
            f"Автор: {news_author}\n"
            f"Дата публікації: {news_time}\n"
            f"Опис: {news_description}\n"
            f"Джерело: {news_source}")
        await state.update_data(count = count + 1)
        await callback.message.edit_text(news_message,reply_markup = news_keyboard)
    else:
        await callback.message.edit_text("Не удалось получить данные о новостях")