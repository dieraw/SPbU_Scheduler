from datetime import datetime
from bs4 import BeautifulSoup


def parse_schedule(html_content):
    # Используем HTML-код напрямую, а не открываем файл
    soup = BeautifulSoup(html_content, 'html.parser')
    lessons = []

    # Получаем даты из заголовков
    for day in soup.find_all('div', class_='panel panel-default'):
        date_header = day.find('h4', class_='panel-title').text.strip()

        # Исправляем формат для строки 'Monday, September 30'
        event_date = datetime.strptime(date_header, "%A, %B %d").date()  # Правильный формат даты

        for event in day.find_all('li', class_='common-list-item row'):
            time = event.find('div', class_='studyevent-datetime').text.strip()
            subject = event.find('div', class_='studyevent-subject').text.strip()

            # Проверка на наличие элемента location
            location_element = event.find('div', class_='studyevent-locations')
            location = location_element.text.strip() if location_element else "Не указано"

            teacher = event.find('div', class_='studyevent-educators').text.strip()
            lessons.append({
                'date': event_date,
                'time': time,
                'subject': subject,
                'location': location,
                'teacher': teacher
            })

    return lessons
