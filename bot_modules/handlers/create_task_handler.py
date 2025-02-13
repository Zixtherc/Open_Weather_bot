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
    wait_for_task = State()

@router.callback_query(F.data == "new_task")
async def create_task(callback : CallbackQuery, state : FSMContext):
    callback.message.answer(' ')
    await callback.message.answer("Введите время заметки, следом введите её текст. Пример : 13.02 13:13 Hello")
    await state.set_state(Form.wait_for_task)

@router.message(Command("new_task"))
async def create_task(message : Message, state : FSMContext):
    await message.answer("Введите время заметки, следом введите её текст. Пример : 13.02 13:13 Hello")
    await state.set_state(Form.wait_for_task)

@router.message(Form.wait_for_task)
async def new_task(message : Message, state : FSMContext):
    chat_id = message.chat.id
    data = await state.get_data()
    user_data = data.get("wait_for_task", message.text)
    ready_data = user_data.split(' ', 2)
    print(f'Это рэди дата которая мне понадобится: {ready_data}')
    task = ready_data[-1]
    date = ready_data[0]
    time = ready_data[1]
    send_time = (date, time)
    await db.add_user(chat_id = chat_id, task = task, send_time = send_time)