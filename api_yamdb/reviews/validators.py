from django.core.exceptions import ValidationError
from django.utils import timezone
from re import findall


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            ('Год выпуска произведения - {} не может быть больше '
             'текущего года - {}!'.format(value, current_year)),
            params={'value': value},
        )
    return value


def validate_username(data):
    PATTERN = r'^[\w.@+-]+\Z'
    if data == 'me':
        raise ValidationError('Имя "me" не использовать!')
    elif len(findall(PATTERN, data)) == 0:
        raise ValidationError('В имени недопустивые символы')
    return data
