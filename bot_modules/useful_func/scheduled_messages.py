import asyncio
import datetime
import time
import colorama
from ..create_bot import bot

async def schedule(chat_id: int, message_text: str, exact_date: str):
    """
    Асинхронна функція для відкладених повідомлень без AsyncIOScheduler.

    :param chat_id: ID чату для надсилання повідомлення.
    :param message_text: Текст повідомлення.
    :param exact_date: Час у форматі 'дд.мм гг:хх', наприклад, '14.02 13:13'.
    """
    try:
        now = datetime.datetime.now()
        send_time = datetime.datetime.strptime(f"{exact_date} {now.year}", "%d.%m %H:%M %Y")
        delay_seconds = int(time.mktime(send_time.timetuple()) - time.mktime(now.timetuple()))

        if delay_seconds < 0:
            print(f'{colorama.Fore.RED} Неверный ввод точного времени, chat_id: {chat_id} {colorama.Style.RESET_ALL}')
            return

        print(f'{colorama.Fore.GREEN} Отложенное сообщение создано, вы в ожидании! {colorama.Style.RESET_ALL}')
        print(f'Время отправки: {exact_date}')
        await asyncio.sleep(delay_seconds)

        await bot.send_message(chat_id=chat_id, text=message_text)

    except Exception as error:
        print(f'Ошибка: {colorama.Fore.RED} {error} {colorama.Style.RESET_ALL}')