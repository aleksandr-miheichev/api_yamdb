from django.core.exceptions import ValidationError
from django.utils import timezone


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
    if data == 'me':
        raise ValidationError('Имя "me" не использовать!')
    return data
