from datetime import datetime


def create_google_calendar_event(service, lesson):
    # Парсим время начала и окончания
    start_time = datetime.strptime(lesson['time'].split('–')[0].strip(), "%H:%M")
    end_time = datetime.strptime(lesson['time'].split('–')[1].strip(), "%H:%M")

    # Дата события
    event_date = "2024-09-29"  # Это можно извлечь из lesson или передавать как параметр
    start = f"{event_date}T{start_time.strftime('%H:%M:%S')}"  # Правильный формат времени
    end = f"{event_date}T{end_time.strftime('%H:%M:%S')}"

    # Проверка времени
    if start_time >= end_time:
        print(f"Ошибка: Время окончания должно быть позже времени начала для занятия '{lesson['subject']}'.")
        return

    # Убедитесь, что location имеет значение
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

    # Попытка вставить событие в календарь
    try:
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Создано событие: {event_result['summary']}")
    except Exception as e:
        print(f"Ошибка при создании события: {e}")
