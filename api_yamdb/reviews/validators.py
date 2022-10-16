from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('Год выпуска произведения: %(value)s не может быть больше '
             'текущего!'),
            params={'value': value},
        )


def validate_username(data):
    if data == 'me':
        raise ValidationError(
            'Имя "me" не использовать!')
    return data
