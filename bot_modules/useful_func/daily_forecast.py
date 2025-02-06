r'''
    :mod:`Модуль`, который вмещает в себя :mod:`функцию` для ежедневной отправки прогноза погоды
'''
# Необходимый импорт для работы с асинхронностью
import asyncio
# Для красивого вывода данных в терминал (не обязательно)
import colorama
# Импортируем объект класса от Bot, для отправки сообщения 
from ..create_bot import bot

import datetime
import time

async def daily_forecast(date: int = None, chat_id : int = None):
    '''
    :mod:`Асинхронная` `функция`, которая позволит нам отправлять `ежедневный` `прогноз` погоды
    '''

   # Используем операторы try, except, для безопасного использования
    try:
        if date:
            now = datetime.datetime.now()
            send_time = datetime.datetime.strptime(f"{date}.{now.year}", "%H.%M")
            print(f'{colorama.Fore.GREEN} Выбранное время : {send_time.strftime("%H:%M")} {colorama.Style.RESET_ALL}')
            delay_second = int(time.mktime(send_time.timetuple()) - time.mktime(now.timetuple()))
            if delay_second < 0:
                print(f'{colorama.Fore.RED} Неверный ввод точного времени, chat_id : {chat_id} {colorama.Style.RESET_ALL}')

    
    # Обрабатываем ошибку, если она возникнет при запросе
    except Exception as error:
        print(f'Ошибка в функции для отложенных сообщений, название ошибки : {colorama.Fore.RED} {error} {colorama.Style.RESET_ALL}')
        return