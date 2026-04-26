import requests
from flask import current_app

def send_phone_otp(phone_no, otp):
    api_key = current_app.config["FAST2SMS_API_KEY"]

    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        "authorization": api_key,
        "route": "otp",
        "variables_values": otp,
        "flash": "0",
        "numbers": phone_no,
    }

    response = requests.get(url, params=payload)

    if response.status_code != 200:
        raise Exception("Failed to send phone OTP")

    return response.json()