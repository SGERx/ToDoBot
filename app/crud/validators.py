import re
from datetime import date


def validate_user_name(name: str):
    if not re.match(r'^[а-яА-Яa-zA-Z]+$', name):
        return 'Имя должно состоять только из букв'


def phone_number_validate(phone_number: str):
    if not re.match(r'^(\+7|8)\d{10}$', phone_number):
        return 'Не корректный номер телефона'


def email_validator(email: str):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return 'Не корректный email'


def validate_user_data(data):
    name_valid = validate_user_name(data.get('name'))
    phone_valid = phone_number_validate(data.get('phone_number'))
    email_valid = email_validator(data.get('email'))
    if name_valid:
        return name_valid
    if phone_valid:
        return phone_valid
    if email_valid:
        return email_valid


def validate_task_data(task_data):
    current_datetime = date.today()

    if task_data.get('task_date') < current_datetime:
        return "Дата задачи не может быть в прошлом!"


def validate_task_name(task_data):
    if not re.match(r'^[а-яА-Яa-zA-Z0-9 №\-]*$', task_data.get('name')):
        return ('Наименование задачи может содержать буквы, '
                'пробелы и знаки "-", "№"')
