# Необходимые импорты для дочерний работы с GoogleApiCalendar
import os
import datetime
# Необходимые импорты для работы с GoogleApiCalendar 
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .create_event_calendar import write_event


# Если мы поменяли read.only, то удаляем token.json, если он создан
SCOPES = ["https://www.googleapis.com/auth/calendar"]


# Функция авторизации 
def authorization():
    creds = None

    # Файл token.json хранит токены доступа и обновления пользователя, и создается автоматически
    # после завершения авторизационного потока в первый раз.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # Если нет доступных (действительных) учетных данных, заставляем пользователя войти в систему.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            # Строим путь к файлу с настройками клиента
            path_to_credentials = os.path.abspath(__file__ + f'../../../static/credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(
                path_to_credentials, SCOPES)
            
            creds = flow.run_local_server(port=0)
        
        # Создаем путь где мы будем создавать токен
        path_to_token = os.path.abspath(__file__ + f'../../../static/token.json')
        # Создаём / обновляем токен ( сейчас он только создаётся )
        with open(path_to_token , "w") as token:
            token.write(creds.to_json())

    # Подключаемся к API календаря
    try:
        service = build("calendar", "v3", credentials=creds)

        # Получаем текущее время в формате UTC
        now = datetime.datetime.utcnow().isoformat() + "Z" 

        # Получаем список событий
        events_result = service.events().list(
            calendarId = "primary",
            timeMin = now,
            maxResults = 5,  # Выбираем сколько всего событий мы хотим получить 
            singleEvents = True,  # Получать только уникальные события (не повторяющиеся)
            orderBy = "startTime",  # Сортировать события по времени начала
        ).execute() # Создаём запрос с помощью функции execute()

        # Получаем список событий из календаря. ??? Как это работает 
        events = events_result.get("items",[])

        # Если нет событий, выводим сообщение и завершаем функцию
        if not events:
            print(events)
            print("Нет ближайших событий.")
            # Завершаем функцию
            # return
            
        
        else:
            print(events)
            print("Вот ближайшие события : ")

            # Перебираем из событий, и выводим его в терминал
            for event in events:
              
              start = event["start"].get("dateTime", event["start"].get("date"))
              print(f"{start} - {event['summary']}")

            # Ссылка где находятся все украинские праздники
            holiday_calendar_id = "en.ukrainian.official#holiday@group.v.calendar.google.com"

            holiday_calendar_id = service.events().list(
                calendarId = holiday_calendar_id,
                timeMin = now,
                maxResults = 5,
                singleEvents = True,
                orderBy = "startTime").execute()
            
            holidays = holiday_calendar_id.get("items",[])

            if not holidays:
                print("Нет ближайших праздничных дней.")
                return
            
            else:
                print("\nБлижайшие праздники")

                # Перебираем из праздников, и выводим их 
                for holiday in holidays:
                    start = holiday["start"].get("dateTime", holiday["start"].get("date"))
                    print(f"{start} - {holiday['summary']}")
        write = write_event(service= service)
        print(write)

    # Отлавливаем ошибки, и выводим их в терминал
    except HttpError as error:
        print(f"Произошла ошибка : {error}")
        
# service = authorization()

