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


def subtract_events(free_start, free_end, events, buffer):
    """
    Start with one free block, subtract each event (with buffer).
    Return list of remaining free blocks as (start, end) tuples.
    """
    free_blocks = [(free_start, free_end)]

    for event in events:
        event_start = datetime.fromisoformat(event["start"]) - timedelta(minutes=buffer)
        event_end = datetime.fromisoformat(event["end"]) + timedelta(minutes=buffer)

        new_free_blocks = []
        for block_start, block_end in free_blocks:
            if event_end <= block_start or event_start >= block_end:
                new_free_blocks.append((block_start, block_end))
            elif event_start <= block_start and event_end >= block_end:
                pass
            elif event_start > block_start and event_end < block_end:
                new_free_blocks.append((block_start, event_start))
                new_free_blocks.append((event_end, block_end))
            elif event_start <= block_start:
                new_free_blocks.append((event_end, block_end))
            elif event_end >= block_end:
                new_free_blocks.append((block_start, event_start))

            pass

        free_blocks = new_free_blocks

    return free_blocks

def round_to_30(dt, direction):
    minute = dt.minute

    if minute == 0 or minute == 30:
        return dt.replace(second=0)

    if direction == "up":
        if minute < 30:
            return dt.replace(minute=30, second=0)
        else:
            return (dt + timedelta(hours=1)).replace(minute=0, second=0)

    if direction == "down":
        if minute < 30:
            return dt.replace(minute=0, second=0)
        else:
            return dt.replace(minute=30, second=0)

def find_available_slots(events, timezone, my_timezone, start_date, end_date, duration, buffer, bh_start, bh_end):
    tz_interviewer = ZoneInfo(SUPPORTED_TIMEZONES[timezone])
    tz_mine = ZoneInfo(my_timezone)

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

        print(f"  DAY: {current_day} | my_start: {my_start} | my_end: {my_end}")

        free_blocks = subtract_events(my_start, my_end, events, buffer)
        for block_start, block_end in free_blocks:
            rounded_start = round_to_30(block_start, "up")
            rounded_end = round_to_30(block_end, "down")

            block_length = (rounded_end - rounded_start).total_seconds() / 60
            if block_length >= duration:
                available_slots.append({
                    "date": current_day,
                    "start": rounded_start,
                    "end": rounded_end,
                    "interviewer_start": rounded_start.astimezone(tz_interviewer),
                    "interviewer_end": rounded_end.astimezone(tz_interviewer),
                })
                



    return available_slots