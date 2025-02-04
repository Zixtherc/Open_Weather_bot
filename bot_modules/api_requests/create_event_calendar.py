# Модуль для отлова ошибок 
from googleapiclient.errors import HttpError

# Создаём функцию записи событий
def write_event(service, 

                event_text: str = "Hello World",  # Название события по умолчанию
                place: str = "Kyiv",  # Местоположение по умолчанию
                description: str = "No description",  # Описание события по умолчанию
                start_time: str = "2024-12-02T09:00:00",  # Время начала события ( по умолчанию — фиксированное время )
                end_time: str = "2024-12-02T10:00:00",  # Время окончания события
                timezone: str = "UTC",  # Часовой пояс по умолчанию
                freq: str = "DAILY",  # Частота повторения события
                interval: int = 1,  # Интервал повторения
                count: int = 1,  # Количество повторений
                email: str = "duckandfiretto@gmail.com",  # Электронная почта участника по умолчанию
                default_reminder: bool = False,  # Использовать ли стандартные напоминания
                window_override: str = "popup",  # Тип напоминания (например, всплывающее окно)
                for_how: int = 10):  # Время перед событием для напоминания (в минутах)

    # Создаём словарь, в который мы будем записывать нужные нам параметры событий
    event = {

        "summary" : event_text, # Название события
        "location" : place, # Местоположение события 
        "description" : description, # Описание событие 

        "start" : {
            "dateTime" : start_time, # Вставляем текущее время 
            "timeZone" : timezone # Указываем часовой пояс
        },

        "end" : {
            "dateTime" : end_time, # Вставляем текущее время
            "timeZone" : timezone # Указываем часовой пояс
        },

        "recurrence" : [{ # Для повторяиющихся событий 
            "freq" : freq, # Частота повторений, можно выставить (Daily, weekly, monthly и т.д)
            "interval" : interval, # Интервал повторения события, каждый первое, (1 день)
            "count" : count # Количество повторений, типа событие повторяется раз в 10 дней и т.д 
        }],
    
        "attendees" : [{
            "email" : email # Электронная почта участников 
        }],

        "reminders" : {
            "useDefault" : default_reminder, # Отключаем использование базовых напоминаний
            "overrides" : [
                {"method": window_override, "minutes" : for_how} # Создаём тип напоминаний, типа как оно будет выглядить, 
                # и за сколько минут будет появляться
            ]}}

    # Пробуем сделать запрос
    try:
        # Тут с переменной мы вставляем все наши приколы
        event = service.events().insert(
            calendarId = "primary", # Выбираем главный календарь ( основной )
            body = event # Передаём все данные о событии, 
        ).execute() # Выполняем запрос 
        print(f'Событие создано: {event.get("htmlLink")}')  # Выводим ссылку на созданное событие
    
     # Обрабатываем ошибку, если она возникнет при запросе
    except HttpError as error: 
        print(f'Произошла ошибка : {error}')  # Выводим ошибку   