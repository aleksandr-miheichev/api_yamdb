from django.core.exceptions import ValidationError
from django.utils import timezone
from re import findall

PATTERN = r'^[\w.@+-]+\Z'
ANTI_PATTERN = r'[^\w.@+-]'


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            ('Год выпуска произведения - {} не может быть больше '
             'текущего года - {}!'.format(value, current_year))
        )
    return value


def validate_username(data):
    if data == 'me':
        raise ValidationError('Имя "me" не использовать!')
    if len(findall(PATTERN, data)) == 0:
        result = list(set(findall(ANTI_PATTERN, data)))
        raise ValidationError(
            f'В имени недопустимые символы: {"".join(result)}'
        )
    return data
