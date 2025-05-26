import logging
from datetime import timedelta
from django.db import connection, models
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from vendors.models import Order, PushSubscription

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def auto_clear_orders():
    try:
        # Ensure DB connection is active
        connection.ensure_connection()
        if not connection.is_usable():
            logger.warning("Database connection is not usable.")
            return
        logger.info("Database connection is active.")

        # Run a lightweight query to confirm connection
        _ = Order.objects.first()

        now = timezone.now()
        one_hour_ago = now - timedelta(hours=1)
        two_hours_ago = now - timedelta(hours=2)

        orders_to_delete = Order.objects.filter(
            models.Q(updated_at__lt=one_hour_ago) | models.Q(created_at__lt=two_hours_ago)
        )

        count = orders_to_delete.count()
        if count > 0:
            logger.info(f"Deleting {count} expired orders...")

            for order in orders_to_delete:
                logger.info(f"Clearing relations for Order {order.token_no}...")

                # Remove relations from PushSubscription
                for sub in order.pushsubscription_set.all():
                    sub.tokens.remove(order)  # Remove specific relation

                # Delete the order
                order.delete()

        # Delete orphaned PushSubscription entries
        orphaned_subs = PushSubscription.objects.annotate(token_count=models.Count('tokens')).filter(token_count=0)
        orphaned_count = orphaned_subs.count()
        if orphaned_count > 0:
            logger.info(f"Deleting {orphaned_count} orphaned PushSubscriptions...")
            orphaned_subs.delete()
        else:
            logger.info("No orphaned PushSubscriptions found.")

    except Exception as e:
        logger.error(f"Error during auto_clear_orders: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_clear_orders, 'interval', minutes=5)  # Run every 5 minutes
    scheduler.start()
    logger.info("Scheduler started, running auto_clear_orders every 5 minutes.")

