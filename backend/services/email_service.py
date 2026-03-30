"""
Email Service
Milestone 7: Email notifications for reminders, reports, and exports
"""

from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)


def send_email(to, subject, html_body, text_body=None):
    """
    Send email using SMTP
    Milestone 7: Email service for notifications
    """
    try:
        # Try to get config from Flask app context
        try:
            mail_server = current_app.config.get('MAIL_SERVER', 'smtp.gmail.com')
            mail_port = current_app.config.get('MAIL_PORT', 587)
            mail_username = current_app.config.get('MAIL_USERNAME', '')
            mail_password = current_app.config.get('MAIL_PASSWORD', '')
            mail_sender = current_app.config.get('MAIL_DEFAULT_SENDER', '')
        except RuntimeError:
            # Fallback if no app context (for Celery tasks)
            import os
            from dotenv import load_dotenv
            load_dotenv()
            mail_server = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
            mail_port = int(os.environ.get('MAIL_PORT', 587))
            mail_username = os.environ.get('MAIL_USERNAME', '')
            mail_password = os.environ.get('MAIL_PASSWORD', '')
            mail_sender = os.environ.get('MAIL_DEFAULT_SENDER', '')
        
        if not mail_username or not mail_password:
            logger.warning("Email credentials not configured. Email not sent.")
            print("[WARNING] Email credentials not configured. Email not sent.")
            return False
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = mail_sender or mail_username
        msg['To'] = to
        
        # Attach text body
        if text_body:
            part1 = MIMEText(text_body, 'plain')
            msg.attach(part1)
        
        # Attach HTML body
        part2 = MIMEText(html_body, 'html')
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(mail_server, mail_port) as server:
            server.starttls()
            server.login(mail_username, mail_password)
            server.sendmail(mail_sender or mail_username, to, msg.as_string())
        
        # No emojis in logger
        logger.info(f"Email sent successfully to {to}")
        print(f"[SUCCESS] Email sent successfully to {to}")
        return True
        
    except Exception as e:
        # No emojis in logger
        logger.error(f"Failed to send email to {to}: {str(e)}")
        print(f"[ERROR] Failed to send email to {to}: {str(e)}")
        return False