import icalendar
from datetime import datetime

# Get today's date and set start/end time
today = datetime.today()
start_time = datetime(today.year, today.month, today.day, 1, 0)
end_time = datetime(today.year, today.month, today.day, 2, 0)

# Define event details
subject = "Meeting Invitation"
location = "Conference Room"
description = "Meeting to discuss project progress"
attendees = ["recipient1@example.com", "recipient2@example.com"]

# Create iCalendar object
cal = Calendar()

# Create event object
event = Event()
event.add('SUMMARY', subject)
event.add('DTSTART', start_time)
event.add('DTEND', end_time)
event.add('LOCATION', location)
event.add('DESCRIPTION', description)
event.add('ORGANIZER', f"mailto:{your_email}")  # Organizer email
for attendee in attendees:
    event.add('ATTENDEE', f"mailto:{attendee}")

# Add event to calendar
cal.add_component(event)

# Save iCalendar data to file
with open('meeting.ics', 'wb') as f:
    f.write(str(cal).encode('utf-8'))

print("Created iCalendar file: meeting.ics")
