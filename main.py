import requests
from schedule_parser import parse_schedule
from google_calendar_auth import google_calendar_auth
from google_calendar_sync import create_google_calendar_event
from lesson_filter import filter_lessons
from subject_exclusion import read_excluded_subjects, write_excluded_subjects

# Укажите URL для получения расписания
SCHEDULE_URL = 'https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/394787/'

def main():
    # Шаг 1: Получение расписания
    print("Получение расписания...")
    response = requests.get(SCHEDULE_URL)

    if response.status_code == 200:
        lessons = parse_schedule(response.text)
        print(f"Найдено {len(lessons)} занятий.")
    else:
        print(f"Ошибка при получении данных: {response.status_code}")
        return

    # Шаг 2: Вывод списка предметов
    unique_subjects = set([lesson['subject'] for lesson in lessons])
    print("\nСписок предметов:")
    for i, subject in enumerate(unique_subjects):
        print(f"{i+1}. {subject}")

    # Чтение исключаемых предметов из файла
    exclude_subjects = read_excluded_subjects()

    # Шаг 3: Фильтрация занятий
    print("Фильтрация ненужных предметов...")
    filtered_lessons = filter_lessons(lessons, exclude_subjects)
    print(f"После фильтрации осталось {len(filtered_lessons)} занятий.")

    # Шаг 7: Добавление предметов в исключения
    add_to_exclude = input("Добавить новые предметы в исключения? (да/нет): ").lower()
    if add_to_exclude == 'да':
        for lesson in lessons:
            if lesson['subject'] not in exclude_subjects:
                exclude_lesson = input(f"Исключить предмет '{lesson['subject']}'? (да/нет): ").lower()
                if exclude_lesson == 'да':
                    exclude_subjects.append(lesson['subject'])
        print("Список исключенных предметов обновлен.")
        write_excluded_subjects(exclude_subjects)

    # Шаг 4: Запрос на синхронизацию
    sync_to_calendar = input("Синхронизировать с Google Calendar? (да/нет): ").lower()
    if sync_to_calendar != 'да':
        print("Синхронизация отменена.")
        return

    # Шаг 5: Авторизация Google Calendar
    print("Авторизация в Google Calendar...")
    service = google_calendar_auth()

    # Шаг 6: Синхронизация занятий
    print("Синхронизация с Google Calendar...")
    for lesson in filtered_lessons:
        create_google_calendar_event(service, lesson)

    print("Завершено!")

if __name__ == "__main__":
    main()