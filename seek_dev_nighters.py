import requests
import pytz
import datetime


def get_number_of_page():
    url = 'https://devman.org/api/challenges/solution_attempts/?page=1'
    request_numb_pages = requests.get(url)
    number_of_pages = request_numb_pages.json()['number_of_pages']
    return number_of_pages


def get_valid_tasks_info(number_of_pages):
    additional_factor = 1
    all_tasks_info = []
    for pages in range(additional_factor, number_of_pages + additional_factor):
        url = 'https://devman.org/api/challenges/solution_attempts'
        parameter = {'page': pages}
        requst_info = requests.get(url, params=parameter)
        page_info = requst_info.json()['records']
        for position in page_info:
            if position.get('timestamp'):
                tasks_info = {
                    'username': position.get('username'),
                    'timestamp': position.get('timestamp'),
                    'timezone': position.get('timezone'),
                }
                all_tasks_info.append(tasks_info)
    return all_tasks_info


def get_midnighters(all_tasks_info):
    midnighters = set()
    s_hours, s_minutes, s_seconds = 0, 0, 0
    e_hours, e_minutes, e_seconds = 6, 0, 0
    period_start = datetime.time(s_hours, s_minutes, s_seconds)
    period_end = datetime.time(e_hours, e_minutes, e_seconds)
    for position in all_tasks_info:
        timestamp = position.get('timestamp')
        timezone = position.get('timezone')
        convert_timestamp = datetime.datetime.utcfromtimestamp(
                float(timestamp))
        utc_datetime_sending = convert_timestamp.replace(tzinfo=pytz.utc)
        real_datetime_sending = utc_datetime_sending.astimezone(
                pytz.timezone(timezone))
        real_time_sending = datetime.datetime.time(real_datetime_sending)
        if period_start <= real_time_sending <= period_end:
            midnighters.add(position.get('username'))
    return midnighters


if __name__ == '__main__':
    number_of_pages = get_number_of_page()
    tasks_info = get_valid_tasks_info(number_of_pages)
    print('List of midnighters: ')
    print(' '.join(get_midnighters(tasks_info)))
