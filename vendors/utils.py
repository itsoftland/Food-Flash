# In orders/utils/push.py
from pywebpush import webpush, WebPushException
from django.conf import settings
import json

import logging
logger = logging.getLogger(__name__)

def send_push_notification(subscription_info, payload):
    try:
        logger.info("Sending push notification with payload: %s to subscription: %s", payload, subscription_info)
        headers = {
            "Content-Type": "application/json"
        }
        webpush(
            subscription_info=subscription_info,
            data=json.dumps(payload),
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims={"sub": "mailto:sanju.softland@gmail.com"},
            headers=headers
        )
        logger.info("Push notification sent successfully.")
        return True
    except WebPushException as ex:
        logger.error("Web push failed: %s", repr(ex))
        return False

