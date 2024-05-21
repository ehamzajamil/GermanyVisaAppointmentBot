import os
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# The URL of the webpage
url = "GERMAN_FOREIGN_OFFICE_APPOINTMENT_SYSTEM_URL"

# Define headers with a user-agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# ScraperAPI key
scraperapi_key = "SCRAPERAPI_KEY"

# Function to check the div count
def check_div_count():
    try:
        response = requests.get(f"http://api.scraperapi.com?api_key={scraperapi_key}&url={url}", headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        wrapper_div = soup.find('div', class_='wrapper')
        div_count = len(wrapper_div.find_all('div'))
        return div_count
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve the webpage. Error: {e}")
        return None

# Function to send email
def send_email(message):
    sender_email = "SENDER_EMAIL"
    receiver_email = "RECEIVER_EMAIL"
    password = "EMAIL_PASSWORD"

    if not sender_email or not receiver_email or not password:
        logging.error("Email credentials not set.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Visa Categories Updated"
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email. Error: {e}")

# Main loop to continuously check the webpage
while True:
    div_count = check_div_count()
    if div_count is not None:
        if div_count != 8:  # Adjust this condition as per your requirement
            message = f"The number of visa categories have been changed."
            send_email(message)
        else:
            logging.info(f"No change in div count. Current count: {div_count}")
    else:
        logging.error("Could not retrieve the div count.")
    
    # Sleep for a specified time before checking again (e.g., 3 minutes)
    time.sleep(200)
