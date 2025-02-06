# Необходимые импорты
from aiogram import  F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import  Command

# Импорты функций
from ..api_requests.request_news import request_news

# Импорты клавиатур 
from ..keyboard.keyboard import news_keyboard

# Импорт состояний для управления вводом пользователя
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# Импортируем объект от класса Router
from ..create_bot import router

# Создаём класс для управления вводом пользователя 
class Form(StatesGroup):
    waiting_for_city = State()
    holiday = State()
    wait_data_diary = State()
    wait_data_news = State()

# Создаём обработчик на callback news
@router.callback_query(F.data == "news")
async def wait_data_news(callback: CallbackQuery, state: FSMContext):
    callback.message.answer(' ')
    await callback.message.answer("Введите страну по которой хотите получить новость, так же введите язык перевода")
    # Устанавливаем состояние
    await state.set_state(Form.wait_data_news)
    
# Создаём обработчик на команду news
@router.message(Command("news"))
async def wait_data_news(message: CallbackQuery, state: FSMContext):
    await message.answer("Введите страну по которой хотите получить новость, так же введите язык перевода")
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
    # На какой язык мы будем переводить
    languange = ready_data[-1]
    # Используем операторы try, except, для безопасного использования
    try:
        # Если в переменной есть какие-то данные
        if country:
            # Вызываем фукнцию, и записываем данные в переменную
            news_info = request_news(country = country, language = languange)
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
                
                await state.update_data(country = country,count_news = count_news)

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
    count_news = data.get('count_news', 0)
    print(count_news)
    count = data.get("count", 0) + 1
    print(count)
    if count >= count_news:
        await callback.answer('Вы достигли максимального значения новостей', show_alert = True)
        return
    country = data.get("country")
    news_info = request_news(country = country, count = count)
    if news_info:
        news_author, news_title, news_description, news_source, news_time, count_news = news_info
        # Группируем переменную для удобной отправки  
        news_message = (
            f"Заголовок: {news_title}\n"
            f"Автор: {news_author}\n"
            f"Дата публікації: {news_time}\n"
            f"Опис: {news_description}\n"
            f"Джерело: {news_source}")
        await state.update_data(count = count)
        await callback.message.edit_text(news_message,reply_markup = news_keyboard)
    else:
        await callback.message.edit_text("Не удалось получить данные о новостях")

@router.callback_query(F.data == "back_news")
async def n_news(callback : CallbackQuery, state : FSMContext):
    data = await state.get_data()
    count_news = data.get('count_news', 0)
    print(count_news)
    count = data.get("count", 0) - 1
    print(count)
    if count < 0:
        await callback.answer('Вы достигли минимального значения новостей', show_alert = True)
        return
    country = data.get("country")
    news_info = request_news(country = country, count = count)
    if news_info:
        news_author, news_title, news_description, news_source, news_time, count_news = news_info
        # Группируем переменную для удобной отправки  
        news_message = (
            f"Заголовок: {news_title}\n"
            f"Автор: {news_author}\n"
            f"Дата публікації: {news_time}\n"
            f"Опис: {news_description}\n"
            f"Джерело: {news_source}")
        await state.update_data(count = count)
        await callback.message.edit_text(news_message,reply_markup = news_keyboard)
    else:
        await callback.message.edit_text("Не удалось получить данные о новостях")