from bot_modules.create_bot import dp, bot
import asyncio
import logging
from bot_modules.handlers import router
from bot_modules.api_requests.google_calendar import authorization
from bot_modules.api_requests.create_event_calendar import write_event

# Функция, которая запускает нашего бота
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

# Запускаем нашего бота, если мы запускаем этот скрипт напрямую, а не импортируем его в другие скрипты
if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    
    # Пытаемся запустить нашего бота с помощью asyncio.run(), так же игнорируем ошибку KeyboardInterrupt
    try:
        asyncio.run(main())
        # Авторизация в гугл календарь
        authorization()
        # Запись данных в этот календарь
        write_event(service= authorization())


    except KeyboardInterrupt:
        print("Bot is shutting down")