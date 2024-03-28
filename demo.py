from O365 import Account, FileSystemTokenBackend

# Set up authentication
credentials = ('your_client_id', 'your_client_secret')
token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.txt')
account = Account(credentials, token_backend=token_backend)

if not account.is_authenticated:
    # Authenticate the account
    account.authenticate(scopes=['basic', 'calendar_all'])
    
# Create a calendar event
calendar = account.schedule()
event = calendar.new_event(
    subject='Meeting Title',
    location='Meeting Room',
    start='2024-04-01T10:00:00',
    end='2024-04-01T12:00:00',
    attendees=['email1@example.com', 'email2@example.com'],
    reminder_minutes_before_start=30,
    busy_status='Busy',
)

# Send the invite
event.save(send_invites=True)
