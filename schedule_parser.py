from bs4 import BeautifulSoup

def parse_schedule(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return parse_schedule_from_soup(soup)

# Вспомогательная функция для парсинга содержимого BeautifulSoup объекта
def parse_schedule_from_soup(soup):
    lessons = []
    for event in soup.find_all('li', class_='common-list-item row'):
        time = event.find('div', class_='studyevent-datetime').text.strip()
        subject = event.find('div', class_='studyevent-subject').text.strip()
        location = event.find('div', class_='studyevent-locations').text.strip()
        teacher = event.find('div', class_='studyevent-educators').text.strip()
        lessons.append({
            'time': time,
            'subject': subject,
            'location': location,
            'teacher': teacher
        })
    return lessons
