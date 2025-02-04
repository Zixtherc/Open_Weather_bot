r'''
:mod:`Модуль`, который вмещает в себя :mod:`функцию` отложенных сообщений, без использования :mod:`AsyncIOScheduler`
'''
# Необходимый импорт для работы с асинхронностью
import asyncio
# Для красивого вывода данных в терминал (не обязательно)
import colorama
# Импортируем объект класса от Bot, для отправки сообщения 
from ..create_bot import bot


async def schedule(schedule_delay : int = 0, chat_id : int = None, message_text : str = None):
    '''
    :mod:`Асинхронная` `функция`, которая позволит нам создать `отложенное сообщение`, не используя модуль `AsyncIOScheduler`
    
    Вмещает в себя параметры
    - :mod:`schedule_delay`: на сколько мы хотим создать отложенное сообщение `(в секундах,пока)` по умолчанию равен нулю
    - :mod:`chat_id`: для `отправки` сообщения по `указанному` chat_id 
    - :mod:`message_text`: `текст` сообщения для `отправки`
    '''

    # Используем операторы try, except, для безопасного использования
    try:
        
        # Выводим данные в терминал (не обязательно)
        print(f'{colorama.Fore.GREEN} Отложенное сообщение создано, вы в ожидании ! {colorama.Style.RESET_ALL}')
        # Переводим секунды в минуты, для использования в asyncio.sleep()
        delay_second = (int(schedule_delay) * 60)
        # Выводим время в терминал (не обязательно)
        print(f'Это делей секонд : {delay_second}')
        # Ожидаем указанное время, используя asyncio.sleep()
        await asyncio.sleep(delay_second)
        # Отправляем сообщение по указанному chat_id, используя bot.send_message()
        await bot.send_message(chat_id = chat_id, text = message_text)
    
    # Обрабатываем ошибку, если она возникнет при запросе
    except Exception as error:
        print(f'Ошибка в функции для отложенных сообщений, название ошибки : {colorama.Fore.RED} {error} {colorama.Style.RESET_ALL}')
        return