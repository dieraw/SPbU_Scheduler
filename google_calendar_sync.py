# google_calendar_sync.py
from datetime import datetime

def create_google_calendar_event(service, lesson):
    # Пример времени события (может потребоваться парсинг)
    start_time = datetime.strptime(lesson['time'].split('–')[0], "%H:%M")
    end_time = datetime.strptime(lesson['time'].split('–')[1], "%H:%M")

    # Дата события
    event_date = "2024-09-30"  # Пример, можно извлечь из файла
    start = f"{event_date}T{start_time.strftime('%H:%M:%S')}:00"
    end = f"{event_date}T{end_time.strftime('%H:%M:%S')}:00"

    event = {
        'summary': lesson['subject'],
        'location': lesson['location'],
        'description': f"Преподаватель: {lesson['teacher']}",
        'start': {
            'dateTime': start,
            'timeZone': 'Europe/Moscow',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'Europe/Moscow',
        },
    }
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Created event: {event_result['summary']}")
