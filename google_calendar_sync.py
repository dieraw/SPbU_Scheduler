from datetime import datetime
import pytz

# Словарь, который связывает предметы с цветами
COLOR_MAP = {
    'Algorithmic methods of graph theory': '1',  # Red
    'Client Technologies for Web Application Development': '2',  # Orange
    # Добавьте другие предметы и соответствующие им colorId
    'Default Subject': '3'  # Yellow
}

def create_google_calendar_event(service, lesson):
    # Определяем часовой пояс Москвы
    moscow_tz = pytz.timezone("Europe/Moscow")

    # Парсим время начала и конца
    start_time_str, end_time_str = lesson['time'].split('–')

    # Используем дату из урока
    event_date = lesson['date']

    # Объединяем дату с распарсенным временем
    start_time = datetime.combine(event_date, datetime.strptime(start_time_str.strip(), "%H:%M").time())
    end_time = datetime.combine(event_date, datetime.strptime(end_time_str.strip(), "%H:%M").time())

    # Форматируем время начала и конца в ISO-формате
    start = start_time.isoformat()
    end = end_time.isoformat()

    # Получаем colorId из COLOR_MAP по названию предмета, или используем значение по умолчанию
    color_id = COLOR_MAP.get(lesson['subject'], '3')  # Используем '3' как цвет по умолчанию

    # Создаем событие
    event = {
        'summary': lesson['subject'],
        'location': lesson['location'] if lesson['location'] else "Не указано",
        'description': f"Преподаватель: {lesson['teacher']}",
        'start': {
            'dateTime': start,
            'timeZone': 'Europe/Moscow',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'Europe/Moscow',
        },
        'colorId': color_id,  # Устанавливаем цвет события
    }

    # Вставляем событие в Google Calendar
    try:
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Создано событие: {event_result['summary']} с цветом ID: {color_id}")
        print(f"Время начала: {start}")
        print(f"Время окончания: {end}")
    except Exception as e:
        print(f"Ошибка при создании события: {e}")

# Пример использования:
# filtered_lessons = [{"subject": "Algorithmic methods of graph theory", ...}]
# for lesson in filtered_lessons:
#     create_google_calendar_event(service, lesson)
