# scheduler.py
import argparse
from config import (
    SUPPORTED_TIMEZONES,
    DEFAULT_BUSINESS_START,
    DEFAULT_BUSINESS_END,
    DEFAULT_DURATION,
    DEFAULT_BUFFER,
)
from slotFinder import find_available_slots
from calendarClient import get_events

def parse_args():
    parser = argparse.ArgumentParser(
        description="Find available interview time slots across time zones"
    )

    parser.add_argument(
        "--timezone", "-tz",
        required=True,
        choices=SUPPORTED_TIMEZONES.keys(),
        help="Interviewer's timezone"
    )

    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=DEFAULT_DURATION,
        help="Interview duration in minutes (default: %(default)s)"
    )

    parser.add_argument(
        "--buffer", "-b",
        type=int,
        default=DEFAULT_BUFFER,
        help="Buffer time in minutes between events (default: %(default)s)"
    )

    parser.add_argument(
        "--start",
        type=str,
        required=True,
        help="Start date for search range (format: YYYY-MM-DD)"
    )

    parser.add_argument(
        "--end",
        type=str,
        required=True,
        help="End date for search range (format: YYYY-MM-DD)"
    )

    parser.add_argument(
        "--bh-start",
        type=int,
        default=DEFAULT_BUSINESS_START,
        help="Business hours start in 24h format (default: %(default)s)"
    )

    parser.add_argument(
        "--bh-end",
        type=int,
        default=DEFAULT_BUSINESS_END,
        help="Business hours end in 24h format (default: %(default)s)"
    )

    return parser.parse_args()

def printFormat(slots, timezone):
    if not slots:
        print("No available slots found.")
        return

    print(f"\nAvailable times ({timezone}):\n")

    current_date = None
    for slot in slots:
        slot_date = slot["interviewer_start"].strftime("%a %b %d")
        start_time = slot["interviewer_start"].strftime("%I:%M %p")
        end_time = slot["interviewer_end"].strftime("%I:%M %p")

        if slot_date != current_date:
            current_date = slot_date
            print(f"  {slot_date}")

        print(f"    {start_time} - {end_time}")

def main():
    args = parse_args()


    print(f"Timezone:       {args.timezone}")
    print(f"Duration:       {args.duration} min")
    print(f"Buffer:         {args.buffer} min")
    print(f"Search range:   {args.start} to {args.end}")
    print(f"Business hours: {args.bh_start}:00 - {args.bh_end}:00")
    mytimezone, events = get_events(args.start, args.end)
    avalible_timeslot = find_available_slots(events, args.timezone, mytimezone, args.start, args.end, args.duration, args.buffer, args.bh_start, args.bh_end)
    printFormat(avalible_timeslot, mytimezone)
if __name__ == "__main__":
    main()