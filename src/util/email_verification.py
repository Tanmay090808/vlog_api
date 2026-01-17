import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from urllib.parse import quote

load_dotenv()
EMAIL_FROM = os.getenv("EMAIL_FROM","")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD","") 
SMTP_SERVER = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")

if not EMAIL_FROM or not EMAIL_PASSWORD:
    raise ValueError("EMAIL_FROM and EMAIL_PASSWORD must be set in environment variables")

def send_verification_email(email: str, token: str):
    safe_token = quote(token)

    verification_link = (
        f"http://localhost:8000/auth/verify-email"
        f"?token={safe_token}"
    )

    body = f"""
Hello,

Please click the link below to verify your email address:

{verification_link}

If you did not create this account, please ignore this email.

Thanks,
Vlog API Team
"""

    message = MIMEText(body, "plain")
    message["Subject"] = "Verify your email"
    message["From"] = EMAIL_FROM
    message["To"] = email 

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server: #type:ignore
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(message)