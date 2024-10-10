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
    unique_subjects = sorted(set(lesson['subject'] for lesson in lessons))
    print("\nСписок предметов:")
    for i, subject in enumerate(unique_subjects):
        print(f"{i + 1}. {subject}")

    # Чтение исключаемых предметов из файла
    exclude_subjects = read_excluded_subjects()

    # Шаг 3: Управление списком исключений
    print("\nТекущий список исключений:", exclude_subjects)
    modify_exclusions = input("Хотите изменить список исключений? (y/n): ").lower()

    if modify_exclusions == 'y':
        while True:
            print("\nВыберите предметы для добавления или удаления из списка исключений.")
            print("Введите номера предметов, разделенные запятой (например, 1,3,5).")
            print("Номера предметов из текущего списка исключений будут удалены, остальные добавлены.")

            # Получаем номера предметов от пользователя
            selected_numbers = input("Введите номера: ").split(',')

            # Проверка на корректность введенных значений
            try:
                selected_indices = [
                    int(num.strip()) - 1 for num in selected_numbers
                    if num.strip().isdigit() and 0 < int(num.strip()) <= len(unique_subjects)
                ]

                # Проверка, что после обработки есть хотя бы один номер
                if not selected_indices:
                    raise ValueError("Введите корректные номера предметов.")

                # Формируем списки для добавления и удаления
                for index in selected_indices:
                    subject = unique_subjects[index]
                    if subject in exclude_subjects:
                        exclude_subjects.remove(subject)  # Удаляем, если уже в исключениях
                    else:
                        exclude_subjects.append(subject)  # Добавляем, если еще нет

                # Обновляем файл исключений
                write_excluded_subjects(exclude_subjects)
                print("Обновленный список исключений:", exclude_subjects)
                break

            except ValueError as e:
                print(f"Ошибка: {e}. Попробуйте снова.")

    # Шаг 4: Фильтрация занятий
    filtered_lessons = filter_lessons(lessons, exclude_subjects)
    print(f"После фильтрации осталось {len(filtered_lessons)} занятий.")

    # Шаг 5: Запрос на синхронизацию
    sync_to_calendar = input("Синхронизировать с Google Calendar? (y/n): ").lower()
    if sync_to_calendar == 'n':
        print("Синхронизация отменена.")
        return

    # Шаг 6: Авторизация Google Calendar
    print("Авторизация в Google Calendar...")
    service = google_calendar_auth()

    # Шаг 7: Синхронизация занятий
    print("Синхронизация с Google Calendar...")
    for lesson in filtered_lessons:
        create_google_calendar_event(service, lesson)

    print("Завершено!")


if __name__ == "__main__":
    main()
