from app.paste.schemas import LifeTime as lt
import datetime as dt
import calendar


def get_days_amount(date, months_amount):
    days = 0
    for i in range(months_amount):
        cur_days = calendar.monthrange(date.year, date.month)[1]
        days += cur_days
        date += dt.timedelta(days=cur_days)
    return days


def get_date_delete(date_creation, lifetime: lt):
    delta = dt.timedelta()

    if lifetime == lt.TEN_MINUTES:
        delta = dt.timedelta(minutes=10)
    elif lifetime == lt.ONE_WEEK:
        delta = dt.timedelta(weeks=1)
    elif lifetime == lt.TWO_WEEKS:
        delta = dt.timedelta(weeks=2)
    elif lifetime == lt.ONE_MONTH:
        days = get_days_amount(date_creation, 1)
        delta = dt.timedelta(days=days)
    elif lifetime == lt.THREE_MONTHS:
        days = get_days_amount(date_creation, 3)
        delta = dt.timedelta(days=days)
    elif lifetime == lt.SIX_MONTHS:
        days = get_days_amount(date_creation, 6)
        delta = dt.timedelta(days=days)
    elif lifetime == lt.ONE_YEAR:
        days = get_days_amount(date_creation, 12)
        delta = dt.timedelta(days=days)

    date_delete = date_creation + delta
    return date_delete
