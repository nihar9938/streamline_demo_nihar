from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
import time

# Define OAuth 2.0 parameters
client_id = 'Your_Client_ID'
redirect_uri = 'http://localhost:8080'  # Should match the redirect URI configured in your app
scope = 'https://graph.microsoft.com/.default'  # Adjust scope based on required permissions
authorization_url = f'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}'

# Configure WebDriver
browser = webdriver.Chrome()  # Use appropriate WebDriver for your browser
browser.get(authorization_url)

# Wait for user to log in and authorize the app
wait = WebDriverWait(browser, 120)
wait.until(EC.url_contains(redirect_uri))

# Extract authorization code from the redirected URL
redirected_url = browser.current_url
parsed_url = urlparse(redirected_url)
authorization_code = parse_qs(parsed_url.query)['code'][0]

print(f'Authorization code obtained: {authorization_code}')

# Close the browser
browser.quit()
