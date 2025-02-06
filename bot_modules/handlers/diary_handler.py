# Необходимые импорты
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import  Command

# Импорт для красивого вывода в терминал (необязательно)
import colorama

# Импорты функций
from ..useful_func.scheduled_messages import schedule

# Импорт состояний для управления вводом пользователя
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# Импортируем объект от класса Router
from ..create_bot import router

# Создаём класс для управления вводом пользователя 
class Form(StatesGroup):
    wait_data_diary = State()

    
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