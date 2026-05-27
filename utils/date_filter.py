# utils/date_filter.py

from datetime import datetime, timedelta


def get_date_range(range_type: str):

    now = datetime.now()

    # =====================================================
    # Daily
    # =====================================================
    if range_type == "daily":

        start = datetime(
            now.year,
            now.month,
            now.day
        )

    # =====================================================
    # Weekly
    # =====================================================
    elif range_type == "weekly":

        start = now - timedelta(days=now.weekday())

        start = datetime(
            start.year,
            start.month,
            start.day
        )

    # =====================================================
    # Monthly
    # =====================================================
    elif range_type == "monthly":

        start = datetime(
            now.year,
            now.month,
            1
        )

    # =====================================================
    # Yearly
    # =====================================================
    elif range_type == "yearly":

        start = datetime(
            now.year,
            1,
            1
        )

    # =====================================================
    # Default Monthly
    # =====================================================
    else:

        start = datetime(
            now.year,
            now.month,
            1
        )

    return start, now