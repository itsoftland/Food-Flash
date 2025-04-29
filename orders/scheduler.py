from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from vendors.models import Order, PushSubscription
from datetime import timedelta
from django.db import models

def auto_clear_orders():
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)
    two_hours_ago = now - timedelta(hours=2)

    # Find orders to delete
    orders_to_delete = Order.objects.filter(
        models.Q(updated_at__lt=one_hour_ago) | models.Q(created_at__lt=two_hours_ago)
    )

    count = orders_to_delete.count()
    if count > 0:
        print(f"Deleting {count} expired orders...")

        for order in orders_to_delete:
            print(f"Clearing relations for Order {order.token_no}...")

            # Remove relations from PushSubscription
            for sub in order.pushsubscription_set.all():
                sub.tokens.remove(order)  # Remove specific relation

            # Delete the order
            order.delete()

    # Delete orphaned PushSubscription entries
    orphaned_subs = PushSubscription.objects.annotate(token_count=models.Count('tokens')).filter(token_count=0)
    orphaned_count = orphaned_subs.count()
    if orphaned_count > 0:
        print(f"Deleting {orphaned_count} orphaned PushSubscriptions...")
        orphaned_subs.delete()

    else:
        print("No orphaned PushSubscriptions found.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_clear_orders, 'interval', minutes=5)  # Run every 5 minutes
    scheduler.start()
