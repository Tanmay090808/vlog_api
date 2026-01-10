import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv()
EMAIL_FROM = os.getenv("EMAIL_FROM","")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD","") 
SMTP_SERVER = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")

if not EMAIL_FROM or not EMAIL_PASSWORD:
    raise ValueError("EMAIL_FROM and EMAIL_PASSWORD must be set in environment variables")

def send_verification_email(to_email, token):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = "Verify your email"
        
        body = f"Your verification token is: {token}"
        msg.attach(MIMEText(body, 'plain'))
        
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise