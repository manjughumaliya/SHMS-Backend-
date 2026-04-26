import smtplib
from email.message import EmailMessage
from flask import current_app

def send_email_otp(to_email, otp):
    sender_email = current_app.config["EMAIL_USER"]
    sender_password = current_app.config["EMAIL_PASSWORD"]

    msg = EmailMessage()
    msg["Subject"] = "Smart Hostel Email OTP"
    msg["From"] = sender_email
    msg["To"] = to_email

    msg.set_content(f"""
Hello,

Your Smart Hostel email verification OTP is:

{otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)