# Необходимые импорты
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import  Command

# Импорт состояний для управления вводом пользователя
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# Импорт объект класса от Database
from ..db_function.class_database import db 

# Импортируем объект от класса Router
from ..create_bot import router

# Создаём класс для управления вводом пользователя 
class Form(StatesGroup):
    update_task = State()

@router.callback_query(F.data == "update_task")
async def create_task(callback : CallbackQuery, state : FSMContext):
    callback.message.answer(' ')
    await callback.message.answer("Введите новое название заметки, и её дату. Пример 13.02 13:13 Hello")
    await state.set_state(Form.update_task)

@router.message(Command("update_task"))
async def create_task(message : Message, state : FSMContext):
    await message.answer("Введите новое название заметки, и её дату. Пример 13.02 13:13 Hello")
    await state.set_state(Form.update_task)

@router.message(Form.update_task)
async def update_task(message : Message, state : FSMContext):
    data = await state.get_data()
    chat_id = message.chat.id
    user_data = data.get('update_task', message.text)
    # Делим текст пользователя по пробелу, 1 раз
    ready_data = user_data.split(' ', 2)
    # Получаем время полученных данных
    send_time = f'{ready_data[0]} {ready_data[1]}'
    text = ready_data[-1]
    flag_succes_upd_task = await db.update_note(chat_id = chat_id, task = text, send_time = send_time)
    if flag_succes_upd_task:
        await message.answer("Заметка успешно изменена")
    else:
        await message.answer("Ошибка при изменении заметки")