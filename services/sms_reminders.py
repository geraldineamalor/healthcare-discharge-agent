from twilio.rest import Client
import os

# Use environment variables (VERY IMPORTANT)
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_SID, TWILIO_AUTH)

def send_sms_mock(number, message):
    print(f"[SMS → {number}] {message}")
