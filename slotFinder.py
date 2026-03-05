# slot_finder.py
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
from config import SUPPORTED_TIMEZONES

def has_conflict(slot, events, buffer):
    for event in events:
        event_start = datetime.fromisoformat(event["start"]) - timedelta(minutes=buffer)
        event_end = datetime.fromisoformat(event["end"]) + timedelta(minutes=buffer)

        if slot["start"] < event_end and event_start < slot["end"]:
            return True

    return False

def find_available_slots(events, timezone, my_timezone, start_date, end_date, duration, buffer, bh_start, bh_end):
    tz_interviewer = ZoneInfo(SUPPORTED_TIMEZONES[timezone])
    tz_mine = ZoneInfo(SUPPORTED_TIMEZONES[my_timezone])

    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    available_slots = []

    for i in range((end - start).days + 1):
        current_day = start + timedelta(days=i)

        if current_day.weekday() >= 5:
            continue

        interviewer_start = datetime(
            current_day.year, current_day.month, current_day.day,
            bh_start, 0, tzinfo=tz_interviewer
        )
        interviewer_end = datetime(
            current_day.year, current_day.month, current_day.day,
            bh_end, 0, tzinfo=tz_interviewer
        )

        my_start = interviewer_start.astimezone(tz_mine)
        my_end = interviewer_end.astimezone(tz_mine)

        slot_start = my_start
        while slot_start + timedelta(minutes=duration) <= my_end:
            slot_end = slot_start + timedelta(minutes=duration)

            slot_candidate = {
                "date": current_day,
                "start": slot_start,
                "end": slot_end,
                "interviewer_start": slot_start.astimezone(tz_interviewer),
                "interviewer_end": slot_end.astimezone(tz_interviewer),
            }

            if not has_conflict(slot_candidate, events, buffer):
                available_slots.append(slot_candidate)

            slot_start = slot_end + timedelta(minutes=buffer)

    return available_slots