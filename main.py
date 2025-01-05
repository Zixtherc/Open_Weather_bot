from bot_modules.create_bot import dp, bot
import asyncio
import logging
from bot_modules.callback_query import router
from bot_modules.api_requests.google_calendar import authorization

# Ошибка с записью событий 
from bot_modules.api_requests.create_event_calendar import write_event
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    
    try:
        asyncio.run(main())
        authorization()
        write_event(service= authorization())


    except Exception as error:
        print(f"Error: {error}")