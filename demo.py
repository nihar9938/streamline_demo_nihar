


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


import requests

# OAuth 2.0 parameters
client_id = 'Your_Client_ID'
client_secret = 'Your_Client_Secret'
redirect_uri = 'Your_Redirect_URI'
scope = 'https://graph.microsoft.com/.default'  # Adjust scope based on required permissions

# Authorization endpoint URL
authorization_url = f'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}'

# Redirect the user to the authorization URL
print('Please log in and authorize access by visiting the following URL:')
print(authorization_url)

# After authorization, get the authorization code from the redirected URI
authorization_code = input('Enter the authorization code from the redirect URI: ')

# Exchange authorization code for access token
token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
token_data = {
    'grant_type': 'authorization_code',
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
    'code': authorization_code,
    'scope': scope
}
token_response = requests.post(token_url, data=token_data)

if token_response.status_code == 200:
    access_token = token_response.json()['access_token']
    print(f'Access token obtained successfully: {access_token}')
else:
    print(f'Error getting access token: {token_response.status_code} - {token_response.text}')
