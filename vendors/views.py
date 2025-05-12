from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import pytz
from .models import Order, Vendor, Device, PushSubscription
from .serializers import OrdersSerializer 
from .utils import send_push_notification
import logging
logger = logging.getLogger(__name__)

def get_current_ist_time():
    ist = pytz.timezone('Asia/Kolkata')
    return timezone.now().astimezone(ist)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_current_time(request):
    current_time = get_current_ist_time()
    return Response({'current_time': current_time.strftime('%Y-%m-%d %H:%M:%S')})

def manage_order(request):
    cache.clear()
    return render(request, 'order_management.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def list_order(request):
    orders = Order.objects.all()  
    serializer = OrdersSerializer(orders, many=True)
    return Response(serializer.data)

from orders.serializers import VendorLogoSerializer  # adjust import if needed
@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_order(request):
    """
    This endpoint updates an existing order's token status to "ready".
    If the order (token) does not exist, it creates a new order with status "ready".
    After updating the order, it sends a push notification to the subscriptions
    associated with that order, unless a recent notification was already sent.
    """
    try:
        data = request.data
        vendor_id = data.get('vendor_id')
        device_id = data.get('device_id')
        counter_no = data.get('counter_no')
        token_no = data.get('token_no')
        status_to_update = data.get('status')

        if not token_no or not status_to_update or not vendor_id or not device_id or not counter_no:
            return Response(
                {"message": "Token number, status, vendor_id, device_id, and counter_no are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch the vendor and device instances
        vendor = Vendor.objects.get(vendor_id=vendor_id)
        device = Device.objects.get(serial_no=device_id)

        try:
            # Try to fetch the existing order
            order = Order.objects.get(token_no=token_no, vendor=vendor.id)
            # Update the order's status and counter number
            order.status = status_to_update
            order.counter_no = counter_no
            order.save()
        except Order.DoesNotExist:
            # Order doesn't exist; create a new order with status "ready"
            new_order_data = {
                'token_no': token_no,
                'vendor': vendor.id,
                'device_id': device.id,
                'counter_no': counter_no,
                'status': "ready"
            }
            serializer = OrdersSerializer(data=new_order_data)
            if serializer.is_valid():
                order = serializer.save()
            else:
                return Response(
                    {"message": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        # Cooldown check (only send if last sent > 1 minute ago)
        should_notify = (
            status_to_update.lower() == "ready" and (
                order.notified_at is None or
                (timezone.now() - order.notified_at) > timedelta(minutes=1)
            )
        )
        if should_notify:
            vendor_serializer = VendorLogoSerializer(vendor, context={'request': request})
            logo_url = vendor_serializer.data.get('logo_url', '')
            subscriptions = PushSubscription.objects.filter(tokens__token_no=token_no).distinct()
            payload = {
                "title": "Order Update",
                "body": f"Your order {token_no} is now ready.",
                "token_no": token_no,
                "status": status_to_update,
                "counter_no": counter_no,
                "name": vendor.name,
                "vendor_id": vendor.vendor_id,
                "location_id": vendor.location_id,
                "logo_url": logo_url,
                "type": "foodstatus"
            }
            push_errors = []

            if subscriptions.exists():  # Only proceed if subscriptions are found
                for subscription in subscriptions:
                    subscription_info = {
                        "endpoint": subscription.endpoint,
                        "keys": {
                            "p256dh": subscription.p256dh,
                            "auth": subscription.auth
                        }
                    }
                    try:
                        send_push_notification(subscription_info, payload)
                    except Exception as e:
                        push_errors.append(str(e))

                order.notified_at = timezone.now()
                order.save(update_fields=['notified_at'])


            if push_errors:
                return Response(
                    {
                        "message": "Order updated, but push notifications encountered errors.",
                        "push_errors": push_errors
                    },
                    status=status.HTTP_207_MULTI_STATUS
                )
        return Response(
            {"message": "Order updated and notifications sent.", "token_no": token_no},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def save_subscription(request):
    data = request.data
    endpoint = data.get("endpoint")
    keys = data.get("keys", {})
    browser_id = data.get("browser_id")
    token_number = data.get("token_number")
    vendor_id = data.get("vendor")  

    if not endpoint or not browser_id or not token_number or not vendor_id:
        return Response({"error": "Invalid subscription data"}, status=400)

    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found."}, status=404)

    # Fetch latest order with matching token_no and vendor
    order = Order.objects.filter(token_no=token_number, vendor=vendor).order_by('-created_at').first()

    if not order:
        return Response({"error": "Order not found."}, status=404)

    # Get or create the subscription
    subscription, _ = PushSubscription.objects.get_or_create(
        browser_id=browser_id,
        defaults={
            "endpoint": endpoint,
            "p256dh": keys.get("p256dh", ""),
            "auth": keys.get("auth", ""),
        },
    )

    # Update subscription fields (if changed)
    subscription.endpoint = endpoint
    subscription.p256dh = keys.get("p256dh", "")
    subscription.auth = keys.get("auth", "")
    subscription.save()

    # Link the subscription to the order
    subscription.tokens.add(order)

    return Response({"message": "Subscription updated successfully."})

@api_view(["POST"])
@permission_classes([AllowAny])
def send_offers(request):
    vendor_id = request.data.get("vendor_id")
    offer = request.data.get("offer")
    title = request.data.get("title")
    if not vendor_id:
        return Response({"message": "Vendor ID is required."}, status=400)

    try:
        vendor = Vendor.objects.get(vendor_id=vendor_id)
    except Vendor.DoesNotExist:
        return Response({"message": "Invalid vendor ID."}, status=404)

    # Serialize logo after vendor is confirmed
    vendor_serializer = VendorLogoSerializer(vendor, context={'request': request})
    logo_url = vendor_serializer.data.get('logo_url', '')

    payload = {
        "title": title,
        "body": offer,
        "name": vendor.name,
        "vendor_id": vendor.vendor_id,
        "location_id": vendor.location_id,
        "logo_url": logo_url,
        "type": "offers",
    }

    # Step 1: Get active orders
    active_orders = Order.objects.filter(vendor=vendor).exclude(status="ready")

    # Step 2: Get distinct subscriptions tied to active orders
    active_subscriptions = PushSubscription.objects.filter(tokens__in=active_orders).distinct()

    logger.info(f"Found {active_subscriptions.count()} subscriptions to notify for vendor {vendor.name}")

    sent_count = 0
    for sub in active_subscriptions:
        subscription_info = {
            "endpoint": sub.endpoint,
            "keys": {
                "p256dh": sub.p256dh,
                "auth": sub.auth,
            },
        }
        success = send_push_notification(subscription_info, payload)
        if success:
            sent_count += 1

    return Response({"message": f"Offer sent to {sent_count} active customers."}, status=200)


