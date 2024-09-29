def filter_lessons(lessons, exclude_subjects):
    return [lesson for lesson in lessons if lesson['subject'] not in exclude_subjects]


if __name__ == "__main__":
    # Пример фильтрации предметов, если запускается отдельно
    lessons = [
        {'subject': 'Теория вероятностей и математическая статистика'},
        {'subject': 'Численные методы'},
    ]
    exclude_subjects = ['Теория вероятностей и математическая статистика']

    filtered_lessons = filter_lessons(lessons, exclude_subjects)
    for lesson in filtered_lessons:
        print(f"Осталось: {lesson['subject']}")
