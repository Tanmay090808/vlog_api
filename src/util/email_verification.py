import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


def get_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Environment variable {name} is not set")
    return value


EMAIL_FROM = get_env("EMAIL_FROM")
EMAIL_PASSWORD = get_env("EMAIL_PASSWORD")
SMTP_HOST = get_env("SMTP_HOST")
SMTP_PORT = int(get_env("SMTP_PORT"))

print("EMAIL_FROM =", EMAIL_FROM)
print("EMAIL_PASSWORD =", EMAIL_PASSWORD)
print("SMTP_HOST =", SMTP_HOST)
print("SMTP_PORT =", SMTP_PORT)


def send_verification_email(email: str, token: str):
    link = f"http://localhost:8000/auth/verify-email?token={token}"

    message = MIMEText(
        f"Click this link to verify your email:\n\n{link}"
    )
    message["Subject"] = "Verify your email"
    message["From"] = EMAIL_FROM
    message["To"] = email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(message)
