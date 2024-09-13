import smtplib
from email.message import EmailMessage
from datetime import datetime
import os
import sys

class Mailogger:
    def __init__(self, identifier: str, 
                 smtp_server: str, sender_email: str, smtp_port: int,
                 receiver_email: str) -> None:
        if 'MAILOG_PASSWORD' not in os.environ:
            print("Please set the MAILOG_PASSWORD environment variable")
            sys.exit(1)
        self.sender_email = sender_email
        self.sender_password = os.environ['MAILOG_PASSWORD']
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.identifier = identifier
        self.receiver_email = receiver_email
    def log(self, subject: str, body: str = '') -> None:
        msg = EmailMessage()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = f'[mailog:{self.identifier}] subject'
        timestamp = datetime.now().strftime(r'%Y-%m-%d %H:%M:%S')
        msg.set_content(body + f'\n---timestamp: {timestamp}---\n')

        # Connect to the server and send the email
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")

class GMailLogger(Mailogger):
    def __init__(self, identifier: str, sender_email: str) -> None:
        super().__init__(identifier, 'smtp.gmail.com', sender_email, 587)
