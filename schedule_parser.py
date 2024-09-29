from bs4 import BeautifulSoup
import requests

def parse_schedule(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    lessons = []

    # Получаем даты из заголовков
    for day in soup.find_all('div', class_='panel panel-default'):
        date_header = day.find('h4', class_='panel-title').text.strip()
        event_date = datetime.strptime(date_header, "%A, %d %B").date()  # Формат даты в заголовке

        for event in day.find_all('li', class_='common-list-item row'):
            time = event.find('div', class_='studyevent-datetime').text.strip()
            subject = event.find('div', class_='studyevent-subject').text.strip()
            location = event.find('div', class_='studyevent-locations').text.strip()
            teacher = event.find('div', class_='studyevent-educators').text.strip()
            lessons.append({
                'date': event_date,
                'time': time,
                'subject': subject,
                'location': location,
                'teacher': teacher
            })

    return lessons
