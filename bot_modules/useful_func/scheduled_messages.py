import asyncio
import colorama
from ..create_bot import bot
async def schedule(schedule_delay : int = 0, chat_id : int = None, message_text : str = None):
    '''
    Асинхронная функция, которая позволит нам создать отложенное сообщение, не используя модуль `AsyncIOScheduler`
    '''
    try:
    
        print(f'{colorama.Fore.GREEN} Отложенное сообщение создано, вы в ожидании ! {colorama.Style.RESET_ALL}')
        delay_second = int(schedule_delay * 60)
        await asyncio.sleep(delay_second)
        await bot.send_message(chat_id = chat_id, text = message_text)
        
    except Exception as error:
        print(f'Ошибка в функции для отложенных сообщений, название ошибки : {colorama.Fore.RED} {error} {colorama.Style.RESET_ALL}')
        return