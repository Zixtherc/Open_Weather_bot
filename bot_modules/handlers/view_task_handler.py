# Необходимые импорты
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import  Command


# Импорт объект класса от Database
from ..db_function.class_database import db 

# Импортируем объект от класса Router
from ..create_bot import router

@router.callback_query(F.data == "view_task")
async def create_task(callback : CallbackQuery):
    callback.message.answer(' ')
    chat_id = callback.message.chat.id
    task, send_time = await db.get_task(chat_id = chat_id)
    await callback.message.answer(f"Ваша заметка на день: {task}, которая будет отправленное в указанное время: {send_time} ")

@router.message(Command("view_task"))
async def create_task(message : Message):
    chat_id = message.chat.id
    task, send_time = await db.get_task(chat_id = chat_id)
    await message.answer(f"Ваша заметка на день: {task}, которая будет отправленное в указанное время: {send_time} ")