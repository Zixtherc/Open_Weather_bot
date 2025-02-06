r'''
    :mod:`Модуль`, который вмещает в себя :mod:`функцию` для ежедневной отправки прогноза погоды
'''
# Необходимый импорт для работы с асинхронностью
import asyncio
# Для красивого вывода данных в терминал (не обязательно)
import colorama
# Импортируем объект класса от Bot, для отправки сообщения 
from ..create_bot import bot

async def daily_forecast():
    '''
    :mod:`Асинхронная` `функция`, которая позволит нам отправлять `ежедневный` `прогноз` погоды
    '''

    try:
        await asyncio.sleep(86400)
    except Exception as error:
        print(f'{colorama.Fore.RED} Ошибка в ежедневной отправки погоды : {error} {colorama.Style.RESET_ALL}')