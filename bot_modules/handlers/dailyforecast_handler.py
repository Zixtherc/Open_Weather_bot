# Необходимые импорты
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import  Command

# Импорт состояний для управления вводом пользователя
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# Импорт функции
from ..useful_func import daily_forecast

# Импортируем объект от класса Router
from ..create_bot import router

# Создаём класс для управления вводом пользователя 
class Form(StatesGroup):
    wait_daily_forecast = State()

@router.callback_query(F.data == "daily_forecast")
async def daily_f(callback : CallbackQuery, state : FSMContext):
    callback.message.answer(' ')
    await callback.message.answer("Введите название города, и время в которое вы хотите получать прогноз")
    await state.set_state(Form.wait_daily_forecast)

@router.message(Command("daily_f"))
async def daily_f(message : Message, state : FSMContext):
    await message.answer("Введите название города, и время в которое вы хотите получать прогноз")
    await state.set_state(Form.wait_daily_forecast)

@router.message(Form.wait_daily_forecast)
async def send_daily_forecast(message : Message, state : FSMContext):
    chat_id = message.chat.id
    date = message.text
    await daily_forecast(date = date , chat_id = chat_id)