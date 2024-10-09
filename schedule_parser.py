from datetime import datetime
from bs4 import BeautifulSoup
import locale


def parse_schedule(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    lessons = []

    # Determine locale based on language
    lang = soup.find('html').get('lang', '')
    try:
        if 'ru' in lang:
            locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        else:
            locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    except locale.Error as e:
        print(f"Locale error: {e}, falling back to default")
        locale.setlocale(locale.LC_TIME, '')

    # Extract current year for parsing
    current_year = datetime.now().year

    for day in soup.find_all('div', class_='panel panel-default'):
        date_header = day.find('h4', class_='panel-title').text.strip()

        # Parse date without year, then adjust if needed
        try:
            if 'ru' in lang:
                event_datetime = datetime.strptime(f"{date_header}", '%A, %d %B')
            else:
                event_datetime = datetime.strptime(f"{date_header}", '%A, %B %d')

            event_date = event_datetime.replace(year=current_year)

            # Adjust for academic year (e.g., October 1–6 implies previous year)
            if event_date.month == 10 and event_date.day < 7:
                event_date = event_date.replace(year=current_year - 1)

        except ValueError as e:
            print(f"Date parsing error: {date_header} — check date format and locale. Error: {e}")
            continue

        # Extract event details for each lesson
        for event in day.find_all('li', class_='common-list-item row'):
            time = event.find('div', class_='studyevent-datetime').text.strip()
            subject = event.find('div', class_='studyevent-subject').text.strip()
            location_element = event.find('div', class_='studyevent-locations')
            location = location_element.text.strip() if location_element else "Not specified"
            teacher = event.find('div', class_='studyevent-educators').text.strip()

            lessons.append({
                'date': event_date,
                'time': time,
                'subject': subject,
                'location': location,
                'teacher': teacher
            })

    return lessons
