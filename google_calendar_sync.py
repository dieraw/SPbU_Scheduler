from datetime import datetime

def create_google_calendar_event(service, lesson):
    # Парсим время начала и окончания занятий из расписания
    start_time_str, end_time_str = lesson['time'].split('–')

    # Дата события, которая была спарсена ранее (lesson['date'] должно быть объектом datetime.date)
    event_date = lesson['date']

    # Комбинируем дату и спарсенное время для получения datetime объектов
    start_time = datetime.combine(event_date, datetime.strptime(start_time_str.strip(), "%H:%M").time())
    end_time = datetime.combine(event_date, datetime.strptime(end_time_str.strip(), "%H:%M").time())

    # Преобразуем в ISO-формат для передачи в Google Calendar
    start = start_time.isoformat()
    end = end_time.isoformat()

    # Проверка на корректность времени
    if start_time >= end_time:
        print(f"Ошибка: Время окончания должно быть позже времени начала для занятия '{lesson['subject']}'.")
        return

    # Получение местоположения, если оно указано
    location = lesson['location'] if lesson['location'] else "Не указано"

    event = {
        'summary': lesson['subject'],
        'location': location,
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

    print(f"Создание события: {event}")  # Отладочный вывод

    # Вставляем событие в Google Calendar
    try:
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Создано событие: {event_result['summary']}")
    except Exception as e:
        print(f"Ошибка при создании события: {e}")
