# Необходимые импорты для работы с GoogleApiCalendar 
import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Если мы поменяли read.only, то удаляем token.json, если он создан
SCOPES = ["https://www.googleapis.com/auth/calendar"]


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
            
            # Строим путь к файлу
            path_to_credentials = os.path.abspath(__file__ + f'../../../static/credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(
                path_to_credentials, SCOPES)
            
            creds = flow.run_local_server(port=0)
        
        # Создаем или обновляем токен
        path_to_token = os.path.abspath(__file__ + f'../../../static/token.json')
        with open(path_to_token , "w") as token:
            token.write(creds.to_json())

    # Подключаемся к API календаря
    try:
        service = build("calendar", "v3", credentials=creds)

        # Получаем текущее время в формате UTC
        now = datetime.datetime.utcnow().isoformat() + "Z" 

        # Получаем список событий
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=20,  # Максимум 20 событий
            singleEvents=True,  # Получать только одноразовые события (не повторяющиеся)
            orderBy="startTime",  # Сортировать события по времени начала
        ).execute()

        events = events_result.get("items", [])

        if not events:
            print("Нет ближайших событий.")
            # Завершаем функцию
            
        
        else:
            print("Вот ближайшие события : ")

            # Перебираем из событий, и выводим его в терминал
            for event in events:
              pass
              # start = event["start"].get("dateTime", event["start"].get("date"))
              # print(f"{start} - {event['summary']}")

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

                for holiday in holidays:
                    start = holiday["start"].get("dateTime", holiday["start"].get("date"))
                    print(f"{start} - {holiday['summary']}")


    except HttpError as error:
        print(f"Произошла ошибка: {error}")