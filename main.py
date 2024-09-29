import requests
from schedule_parser import parse_schedule
from google_calendar_auth import google_calendar_auth
from google_calendar_sync import create_google_calendar_event
from lesson_filter import filter_lessons

# Укажите URL для получения расписания
SCHEDULE_URL = 'https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/394787/'  # Замените на нужный URL

# Перечень предметов, которые нужно исключить
EXCLUDE_SUBJECTS = [
    'Теория вероятностей и математическая статистика',  # Пример
    'Численные методы'  # Добавьте любые предметы, которые не нужно синхронизировать
]


def main():
    # Шаг 1: Получение расписания
    print("Получение расписания...")
    url = "https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/394787/"  # Пример URL
    response = requests.get(url)

    lessons = None  # Инициализируем переменную
    if response.status_code == 200:
        # Парсим HTML-контент напрямую
        lessons = parse_schedule(response.text)
        print(f"Найдено {len(lessons)} занятий.")
    else:
        print(f"Ошибка при получении данных: {response.status_code}")
        return  # Выходим из программы, если данные не удалось получить

    # Шаг 2: Фильтрация занятий
    if lessons:
        print("Фильтрация ненужных предметов...")
        filtered_lessons = filter_lessons(lessons, EXCLUDE_SUBJECTS)
        print(f"После фильтрации осталось {len(filtered_lessons)} занятий.")
    else:
        print("Нет занятий для фильтрации.")
        return  # Выходим, если занятий нет

    # Шаг 3: Авторизация Google Calendar
    print("Авторизация в Google Calendar...")
    service = google_calendar_auth()

    # Шаг 4: Синхронизация занятий с Google Calendar
    print("Синхронизация с Google Calendar...")
    for lesson in filtered_lessons:
        create_google_calendar_event(service, lesson)

    print("Все события успешно добавлены в Google Calendar!")


if __name__ == "__main__":
    main()
