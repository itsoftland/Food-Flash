# static/utils/functions/utils.py
from datetime import timedelta,datetime
from django.utils import timezone

def get_time_ranges():
    now = timezone.now()
    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return start_of_today, start_of_week, start_of_month

def get_filtered_date_range(date_range, from_date_str=None, to_date_str=None):
    """
    Returns a (start, end) datetime tuple based on the date_range value.
    If range is 'custom', it uses from_date_str and to_date_str (YYYY-MM-DD).
    """
    now = timezone.now()
    start_of_today, start_of_week, start_of_month = get_time_ranges()

    if date_range == 'today':
        return start_of_today, now
    elif date_range == 'this_week':
        return start_of_week, now
    elif date_range == 'this_month':
        return start_of_month, now
    elif date_range == 'custom':
        try:
            from_dt = timezone.make_aware(datetime.strptime(from_date_str, "%Y-%m-%d"))
            to_dt = timezone.make_aware(datetime.strptime(to_date_str, "%Y-%m-%d") + timedelta(days=1))
            return from_dt, to_dt
        except (ValueError, TypeError):
            return None, None
    return None, None
