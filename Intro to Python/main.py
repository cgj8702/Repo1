import datetime
from bday_messages import random_message

today = datetime.date.today()
next_birthday = datetime.date(2026, 8, 7)

days_away = next_birthday - today

if today == next_birthday:
    print(random_message)
else:
    print(f'My next birthday is', {days_away.days}, ' days away')
