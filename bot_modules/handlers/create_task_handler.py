# Необходимые импорты
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import  Command

# Импорт состояний для управления вводом пользователя
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# Импорт объект класса от DataBase
from ..db_function.class_database import db 

# Импортируем объект от класса Router
from ..create_bot import router

# Создаём класс для управления вводом пользователя 
class Form(StatesGroup):
    wait_for_task = State()

@router.callback_query(F.data == "new_task")
async def daily_f(callback : CallbackQuery, state : FSMContext):
    callback.message.answer(' ')
    await callback.message.answer("Введите название города, и время в которое вы хотите получать прогноз")
    await state.set_state(Form.wait_for_task)

@router.message(Command("new_task"))
async def daily_f(message : Message, state : FSMContext):
    await message.answer("Введите название заметки которую вы хотите добавить, так же введите время в которое оно к вам придёт")
    await state.set_state(Form.wait_for_task)

@router.message(Form.wait_for_task)
async def send_daily_forecast(message : Message, state : FSMContext):
    chat_id = message.chat.id
    data = await state.get_data()
    user_data = await data.get("wait_for_task")
    ready_data = user_data.split(' ', 1)
    