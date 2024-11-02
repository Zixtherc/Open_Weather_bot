from bot_modules.create_bot import dp, bot
import asyncio
import logging
from bot_modules.callback_query import router

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")