r'''
:mod:`Модуль`, который вмещает в себя :mod:`функцию` отложенных сообщений, без использования :mod:`AsyncIOScheduler`
'''
# Необходимый импорт для работы с асинхронностью
import asyncio
# Для красивого вывода данных в терминал (не обязательно)
import colorama
# Импортируем объект класса от Bot, для отправки сообщения 
from ..create_bot import bot
# Встроенный модуль python, который поможет нам преобразовать дату, по типу 06.02, в секунды 
import datetime
import time

async def schedule(chat_id : int = None, message_text : str = None, exact_date: str = None):
    r'''
    :mod:`Асинхронная` `функция`, которая позволит нам создать `отложенное сообщение`, не используя модуль `AsyncIOScheduler`
    
    Вмещает в себя параметры: 
    - :mod:`chat_id`: для `отправки` сообщения по `указанному` chat_id 
    - :mod:`message_text`: `текст` сообщения для `отправки`
    - :mod:`exact_date`: `точная` дата и время в формате `год-месяц-день` часы:минуты:секунды, например, `'2025-02-06 12:30:00'`

    Пример использования : 
    ```python
    await schedule(chat_id = 123456789, message_text = "Привет мир!", exact_date = "05.02 13.13")
    '''

    # Используем операторы try, except, для безопасного использования
    try:
        if exact_date:
            now = datetime.datetime.now()
            send_time = datetime.datetime.strptime(f"{exact_date}.{now.year}", "%d.%m.%H.%M.%Y")
            delay_second = int(time.mktime(send_time.timetuple()) - time.mktime(now.timetuple()))
            if delay_second < 0:
                print(f'{colorama.Fore.RED} Неверный ввод точного времени, chat_id : {chat_id} {colorama.Style.RESET_ALL}')

            print(f'{colorama.Fore.GREEN} Отложенное сообщение создано, вы в ожидании ! {colorama.Style.RESET_ALL}')
            # Ожидаем указанное время, используя asyncio.sleep()
            await asyncio.sleep(delay_second)
            # Отправляем сообщение по указанному chat_id, используя bot.send_message()
            await bot.send_message(chat_id = chat_id, text = message_text)
    
    # Обрабатываем ошибку, если она возникнет при запросе
    except Exception as error:
        print(f'Ошибка в функции для отложенных сообщений, название ошибки : {colorama.Fore.RED} {error} {colorama.Style.RESET_ALL}')
        return