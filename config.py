# config.py

# Business hours
DEFAULT_BUSINESS_START = 10
DEFAULT_BUSINESS_END = 17

# Scheduling defaults
DEFAULT_DURATION = 60
DEFAULT_BUFFER = 60
DEFAULT_SEARCH_DAYS = 14

# Supported timezones: display name -> IANA identifier
SUPPORTED_TIMEZONES = {
    "US Eastern": "America/New_York",
    "US Central": "America/Chicago",
    "US Mountain": "America/Denver",
    "US Pacific": "America/Los_Angeles",
    "Japan": "Asia/Tokyo",
    "China": "Asia/Shanghai",
    "South Korea": "Asia/Seoul",
    "India": "Asia/Kolkata",
    "Singapore": "Asia/Singapore",
    "UK": "Europe/London",
    "Central Europe": "Europe/Berlin",
    "Australia": "Australia/Sydney",
}