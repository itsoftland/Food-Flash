from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from vendors.models import Order
from datetime import timedelta
from django.db import models

def auto_clear_orders():
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=2)
    two_hours_ago = now - timedelta(hours=2)

    # Find orders that are older than 1 hour (since status update) OR older than 2 hours (since creation)
    orders_to_delete = Order.objects.filter(
        models.Q(updated_at__lt=one_hour_ago) | models.Q(created_at__lt=two_hours_ago)
    )

    count = orders_to_delete.count()
    if count > 0:
        print(f"Deleting {count} expired orders...")

        for order in orders_to_delete:
            print(f"Deleting Order {order.token_no} and related PushSubscription data...")

            # Delete related PushSubscription tokens (clear the Many-to-Many relationship)
            order.pushsubscription_set.clear()

            # Delete the related PushSubscription itself
            order.pushsubscription_set.all().delete()  # Deletes all related PushSubscriptions

            # Now delete the order itself
            order.delete()
    else:
        print("No expired orders found.")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_clear_orders, 'interval', minutes=1)  # Run every 5 minutes
    scheduler.start()
