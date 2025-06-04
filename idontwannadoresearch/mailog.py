import smtplib
from email.message import EmailMessage
from datetime import datetime
import os
import sys
import logging
import tomllib

class MailLogger:
    @staticmethod
    def load_from_config(id: str, file: str, chained_logger: logging.Logger | None = None) -> 'MailLogger':
        with open(file, 'rb') as f:
            config = tomllib.load(f)
        logging_config = config.get('logging', {})
        disabled = not logging_config.get('enable_email', False)
        email_send = logging_config.get('email_send', None)
        email_receive = logging_config.get('email_receive', None)
        email_smtp_server = logging_config.get('email_smtp_server', 'smtp.gmail.com')
        email_smtp_port = logging_config.get('email_smtp_port', 587)
        email_smtp_password = logging_config.get('email_smtp_password', None)
        return MailLogger(
            identifier=id,
            smtp_server=email_smtp_server,
            sender_email=email_send,
            smtp_port=email_smtp_port,
            receiver_email=email_receive,
            chained_logger=chained_logger,
            disabled=disabled,
            password=email_smtp_password
        )

    def __init__(self, identifier: str, 
                 smtp_server: str, sender_email: str, smtp_port: int,
                 receiver_email: str, chained_logger: logging.Logger | None = None,
                 disabled: bool | None = None, password: str | None = None) -> None:
        if (disabled is not None and disabled) or 'MAILOG_DISABLE' in os.environ and os.environ['MAILOG_DISABLE'] == '1':
            self.disabled = True
        else:
            self.disabled = False
        if not self.disabled and password = None and 'MAILOG_PASSWORD' not in os.environ:
            print("Please set the MAILOG_PASSWORD environment variable")
            sys.exit(1)
        self.sender_email = sender_email
        if not self.disabled:
            self.sender_password = os.environ['MAILOG_PASSWORD'] if password is None else password
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

class GMailLogger(MailLogger):
    def __init__(self, identifier: str, sender_email: str, receiver_email, chained_logger: logging.Logger | None = None) -> None:
        super().__init__(identifier=identifier, smtp_server='smtp.gmail.com', sender_email=sender_email, 
                         smtp_port=587, receiver_email=receiver_email, chained_logger=chained_logger)
