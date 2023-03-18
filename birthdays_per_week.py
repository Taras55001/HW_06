from datetime import datetime, timedelta
from faker import Faker
from pprint import pprint


def get_birthdays_per_week(users):
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday()) + timedelta(7)
    week_end = week_start + timedelta(days=5)
    saturday = week_start - timedelta(days=2)
    sunday = week_start - timedelta(days=1)
    birthdays = []
    birthdays_weekend = []

    for user in users:
        bd = datetime.combine(user['birthday'], datetime.min.time())
        if week_start <= bd.replace(year=datetime.now().year) <= week_end:
            birthdays.append(user)
        elif saturday <= bd.replace(year=datetime.now().year) <= sunday:
            birthdays_weekend.append(user)

    if birthdays_weekend:
        print(
            f"Birthdays in Saturday and Sunday ({saturday.strftime('%Y-%m-%d')} - {sunday.strftime('%Y-%m-%d')}):")
        for user in birthdays_weekend:
            print(user['name'], user['birthday'].strftime('%Y-%m-%d'))

    if birthdays:
        print(
            f"Birthdays in the next week ({week_start.strftime('%Y-%m-%d')} - {week_end.strftime('%Y-%m-%d')}):")

        for user in birthdays:
            print(user['name'], user['birthday'].strftime('%Y-%m-%d'))
    else:
        print("No birthdays in the next week")


user = {}
fake = Faker('uk_UA')

users = []
for _ in range(365):
    user = {}
    user['name'] = fake.name()
    user['birthday'] = fake.date_of_birth(minimum_age=1, maximum_age=165)
    users.append(user)

if __name__ == "__main__":

    result = get_birthdays_per_week(users)
