from django.utils import timezone


def get_current_year():
    date = timezone.now().date()
    return date.year


def get_current_month():
    date = timezone.now().date()
    return date.month
