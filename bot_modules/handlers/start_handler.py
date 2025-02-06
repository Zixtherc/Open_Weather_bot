# Необходимые импорты
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

# Импортируем объект от класса Router
from ..create_bot import router

# Импорты клавиатур 
from ..keyboard.keyboard import inline_keyboard


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