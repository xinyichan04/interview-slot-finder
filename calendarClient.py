# calendar_client.py
import os
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_calendar_service():
    """Authenticate and return a Google Calendar service object."""
    creds = None

    # token.json stores your access token after first login
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If no valid creds, do the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for next time
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

def get_events(start_date, end_date):
    service = get_calendar_service()
    calendar = service.calendars().get(calendarId="primary").execute()
    mytimezone = calendar["timeZone"]

    time_min = f"{start_date}T00:00:00Z"
    time_max = f"{end_date}T23:59:59Z"

    calendar_list = service.calendarList().list().execute()

    formatted = []
    for cal in calendar_list.get("items", []):
        cal_id = cal["id"]
        events_result = service.events().list(
            calendarId=cal_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        for event in events_result.get("items", []):
            if "dateTime" not in event["start"]:
                continue

            formatted.append({
                "summary": event.get("summary", "Busy"),
                "start": event["start"]["dateTime"],
                "end": event["end"]["dateTime"],
            })

    for event in formatted:
        print(f"  EVENT: {event['summary']} | {event['start']} → {event['end']}")

    return mytimezone, formatted