# orders/utils/push.py
from pywebpush import webpush, WebPushException
from django.conf import settings
from .models import PushSubscription
import json
import logging

logger = logging.getLogger(__name__)

def notify_web_push(order, vendor, payload):
    subscriptions = PushSubscription.objects.filter(tokens__token_no=order.token_no, tokens__vendor=vendor).distinct()
    errors = []
    for sub in subscriptions:
        try:
            send_push_notification({
                "endpoint": sub.endpoint,
                "keys": {"p256dh": sub.p256dh, "auth": sub.auth}
            }, payload)
        except Exception as e:
            logger.error(f"Push failed: {e}")
            errors.append(str(e))
    return errors

def send_push_notification(subscription_info, payload):
    try:
        logger.info("Attempting to send web push notification.")
        logger.debug("Payload: %s", json.dumps(payload, indent=2))
        logger.debug("Subscription Info: %s", json.dumps(subscription_info, indent=2))

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

        logger.info("Web push notification sent successfully.")
        return True

    except WebPushException as ex:
        logger.error("Web push failed for subscription: %s", subscription_info)
        logger.exception("Exception during web push: %s", repr(ex))
        return False

    except Exception as e:
        logger.exception("Unexpected error in web push notification: %s", str(e))
        return False
# from pywebpush import webpush, WebPushException
# from django.conf import settings
# from .models import PushSubscription
# import json
# import logging

# logger = logging.getLogger(__name__)

# def notify_web_push(order, vendor, payload):
#     subscriptions = PushSubscription.objects.filter(
#         tokens__token_no=order.token_no, 
#         tokens__vendor=vendor
#     ).distinct()

#     subscription_list = [
#         {
#             "endpoint": sub.endpoint,
#             "keys": {"p256dh": sub.p256dh, "auth": sub.auth}
#         }
#         for sub in subscriptions
#     ]

#     return send_push_notification(subscription_list, payload)


# def send_push_notification(subscription_list, payload):
#     errors = []
#     logger.info(f"Sending web push to {len(subscription_list)} subscriptions")

#     for subscription_info in subscription_list:
#         try:
#             logger.debug("Payload: %s", json.dumps(payload, indent=2))
#             logger.debug("Subscription Info: %s", json.dumps(subscription_info, indent=2))

#             headers = {
#                 "Content-Type": "application/json"
#             }

#             webpush(
#                 subscription_info=subscription_info,
#                 data=json.dumps(payload),
#                 vapid_private_key=settings.VAPID_PRIVATE_KEY,
#                 vapid_claims={"sub": "mailto:sanju.softland@gmail.com"},
#                 headers=headers
#             )

#             logger.info("Web push sent to one subscription successfully.")

#         except WebPushException as ex:
#             logger.error("Web push failed for subscription: %s", subscription_info)
#             logger.exception("WebPushException: %s", repr(ex))
#             errors.append(str(ex))

#         except Exception as e:
#             logger.exception("Unexpected error: %s", str(e))
#             errors.append(str(e))

#     return errors
