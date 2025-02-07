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

async def daily_forecast(date: int = None, chat_id : int = None):
    '''
    :mod:`Асинхронная` `функция`, которая позволит нам отправлять `ежедневный` `прогноз` 
    
    Вмещает в себя параметры: 
    - :mod: `date`: `точная` дата и время в формате `год-месяц-день` часы:минуты:секунды, например, `'2025-02-06 12:30:00'`
    - :mod: `chat_id`: для `отправки` сообщения по `указанному` chat_id
    '''

    # Используем операторы try, except, для безопасного использования 2025.02.07 14.14.14
    # try:
    if date:
        date_send = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        delay = (date_send - now).total_seconds()

        if delay < 0:
            print(f'{colorama.Fore.RED} Неверный ввод точного времени, chat_id : {chat_id} {colorama.Style.RESET_ALL}')
            return
        await bot.send_message(chat_id = chat_id, text = "Test")
    else:
        bot.send_message(chat_id = chat_id, text = "Неверный ввод,проверьте всё заново, и отправьте сначало")
    
    # Обрабатываем ошибку, если она возникнет при запросе
    # except Exception as error:
    #     print(f'Ошибка в функции для прогноза погоды ежедневно , название ошибки : {colorama.Fore.RED} {error} {colorama.Style.RESET_ALL}')
        # return