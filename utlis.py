from flask_mail import Message as MailMessage
import string
import random

# Utility functions
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_email(mail, to_email, subject, content):
    msg = MailMessage(subject=subject, recipients=[to_email], body=content)
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False