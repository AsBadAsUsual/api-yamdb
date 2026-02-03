import datetime as dt

from django.core.exceptions import ValidationError

from .constants import MIN_SCORE, MAX_SCORE


def validate_year(value):
    if value > dt.date.today().year:
        raise ValidationError("Нельзя добавлять произведения будущего!")


def validate_score(value):
    if value < MIN_SCORE or value > MAX_SCORE:
        raise ValidationError("Оценка должна быть от "
                              f"{MIN_SCORE} до {MAX_SCORE}")
