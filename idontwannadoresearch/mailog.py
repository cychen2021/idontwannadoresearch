import smtplib
from email.message import EmailMessage
from datetime import datetime
import os
import sys
import logging

class Mailogger:
    def __init__(self, identifier: str, 
                 smtp_server: str, sender_email: str, smtp_port: int,
                 receiver_email: str, chained_logger: logging.Logger | None = None) -> None:
        if 'MAILOG_DISABLE' in os.environ and os.environ['MAILOG_DISABLE'] == '1':
            self.disabled = True
        if not self.disabled and 'MAILOG_PASSWORD' not in os.environ:
            print("Please set the MAILOG_PASSWORD environment variable")
            sys.exit(1)
        self.sender_email = sender_email
        self.sender_password = os.environ['MAILOG_PASSWORD']
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.identifier = identifier
        self.receiver_email = receiver_email
        self.chained_logger = chained_logger
    def log(self, subject: str, body: str = '') -> None:
        msg = EmailMessage()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email

        timestamp = datetime.now().strftime(r'%Y-%m-%d %H:%M:%S')
        header = f'[mailog:{self.identifier}] {subject}'
        body = body + f'\n---timestamp: {timestamp}---\n'
        
        msg['Subject'] = header
        msg.set_content(body)

        if self.chained_logger is not None:
            self.chained_logger.info(header)
            self.chained_logger.info(body)

        if self.disabled :
            return
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
    def __init__(self, identifier: str, sender_email: str, receiver_email, chained_logger: logging.Logger | None = None) -> None:
        super().__init__(identifier=identifier, smtp_server='smtp.gmail.com', sender_email=sender_email, 
                         smtp_port=587, receiver_email=receiver_email, chained_logger=chained_logger)
