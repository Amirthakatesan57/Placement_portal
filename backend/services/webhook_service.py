"""
Webhook Service
Milestone 7: Google Chat webhook notifications
"""

import requests
import logging

logger = logging.getLogger(__name__)


def send_gchat_notification(webhook_url, message):
    """
    Send notification to Google Chat via webhook
    Milestone 7: GChat notifications for reminders
    """
    try:
        response = requests.post(
            webhook_url,
            json=message,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            logger.info("GChat notification sent successfully")
            return True
        else:
            logger.error(f"GChat notification failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"Failed to send GChat notification: {str(e)}")
        return False