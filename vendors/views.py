from django.shortcuts import render
from .models import Order,Vendor,Device, PushSubscription
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import OrdersSerializer 
from rest_framework import status
from django.core.cache import cache
from django.utils import timezone
import pytz

def get_current_ist_time():
    ist = pytz.timezone('Asia/Kolkata')
    return timezone.now().astimezone(ist)  # Convert UTC to IST

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

from .utils import send_push_notification

@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_order(request):
    """
    This endpoint updates an existing order's token status to "ready".
    If the order (token) does not exist, it creates a new order with status "ready".
    After updating the order, it sends a push notification to the subscriptions
    associated with that order.
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
                serializer.save()
            else:
                return Response(
                    {"message": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # After updating/creating the order, send push notifications
        subscriptions = PushSubscription.objects.filter(tokens__token_no=token_no)
        # payload = "Your order is ready!" 
        payload = {
            "title": "Order Update",
            "body": f"Your order {token_no} is now ready.",
            "token_no": token_no,
            "status": status_to_update,
            "counter_no": counter_no,
            "name":vendor.name
        }
        push_errors = []

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

        # Decide the response based on whether push notifications succeeded.
        if push_errors:
            return Response(
                {
                    "message": "Order updated, but push notifications encountered errors.",
                    "push_errors": push_errors
                },
                status=status.HTTP_207_MULTI_STATUS
            )
        else:
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

# In orders/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import send_push_notification
import logging
logger = logging.getLogger(__name__)

@api_view(["POST"])
@permission_classes([AllowAny])
def test_push_notification(request):
    logger.info("Received test push request with data: %s", request.data)
    subscription_info = {
        "endpoint": request.data.get("endpoint"),
        "keys": {
            "p256dh": request.data.get("p256dh"),
            "auth": request.data.get("auth"),
        },
    }
    payload = {
        "title": "Test Notification",
        "body": "This is a test push from the API.",
    }
    success = send_push_notification(subscription_info, payload)
    if success:
        logger.info("Test push sent successfully for subscription: %s", subscription_info)
        return Response({"message": "Test push sent successfully."}, status=200)
    else:
        logger.error("Failed to send test push for subscription: %s", subscription_info)
        return Response({"message": "Failed to send test push."}, status=400)
