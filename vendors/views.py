import json
import logging
from datetime import timedelta

from django.core.cache import cache
from django.shortcuts import render
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Order, Vendor, Device, AndroidDevice, PushSubscription, AdminOutlet, AndroidAPK
from .serializers import OrdersSerializer
from orders.serializers import VendorLogoSerializer
from .utils import send_push_notification, notify_web_push

logger = logging.getLogger(__name__)

from django.utils.timezone import now, localtime
from datetime import timedelta
import threading

_current_time_cache = {
    "time": None,
    "expires_at": None,
    "lock": threading.Lock()
}

@api_view(['GET'])
@permission_classes([AllowAny])
def get_current_time(request):
    with _current_time_cache["lock"]:
        current = now()
        if (_current_time_cache["time"] is None or
            _current_time_cache["expires_at"] < current):
            
            # Cache refresh
            current_ist = localtime(current)  # IST as per TIME_ZONE
            _current_time_cache["time"] = current_ist.strftime('%Y-%m-%d %H:%M:%S')
            _current_time_cache["expires_at"] = current + timedelta(seconds=5)  # 5-sec cache
        
        return Response({'current_time': _current_time_cache["time"]})


def manage_order(request):
    cache.clear()
    return render(request, 'order_management.html')

@api_view(['GET'])
@permission_classes([AllowAny])
def list_order(request):
    orders = Order.objects.all()  
    serializer = OrdersSerializer(orders, many=True)
    return Response(serializer.data) 

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

@api_view(['POST'])
@permission_classes([AllowAny])
def register_device(request):
    serial_no = request.data.get('serial_no')
    customer_id = request.data.get('customer_id')

    request_ip = request.META.get('REMOTE_ADDR', 'Unknown')
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    logger.info("Device registration attempt from IP: %s | User-Agent: %s", request_ip, user_agent)
    logger.debug("Incoming data — Serial No: %s, Customer ID: %s", serial_no, customer_id)

    if not serial_no or not customer_id:
        logger.warning("Missing fields: serial_no=%s, customer_id=%s", serial_no, customer_id)
        return Response({"error": "Fields 'serial_no' and 'customer_id' are required."}, status=400)

    try:
        # Step 1: Validate customer
        customer = AdminOutlet.objects.get(customer_id=customer_id)
        logger.info("Validated customer: %s", customer_id)

        try:
            # Step 2: Check if device exists with this serial_no
            existing_device = Device.objects.get(serial_no=serial_no)
            logger.info("Device with serial %s already exists", serial_no)

            if existing_device.admin_outlet == customer:
                if existing_device.vendor is not None:
                    logger.info("Device already mapped to vendor: %s", existing_device.vendor.vendor_id)
                    return Response({
                        "status": "Device is already registered and mapped to vendor.",
                        "mapped": True,
                        "vendor_id": existing_device.vendor.vendor_id,
                        "vendor_name": existing_device.vendor.name,
                    }, status=200)
                else:
                    logger.info("Device is registered but not mapped to any vendor.")
                    return Response({
                        "status": "Device is already registered but not yet mapped to a vendor.",
                        "mapped": False,
                        "vendor_id": None,
                        "vendor_name": None,
                    }, status=200)
            else:
                logger.warning("Device serial conflict: Already registered with another customer.")
                return Response({
                    "error": "Serial number already registered with another customer."
                }, status=409)

        except Device.DoesNotExist:
            # Step 4: New device, create it
            device = Device.objects.create(
                serial_no=serial_no,
                admin_outlet=customer,
                vendor=None
            )
            logger.info("New device registered: %s for customer: %s", serial_no, customer_id)
            return Response({
                "status": "Device is registered but not yet mapped to a vendor.",
                "mapped": False,
                "vendor_id": None,
                "vendor_name": None,
            }, status=201)

    except AdminOutlet.DoesNotExist:
        logger.error("Customer not found: %s", customer_id)
        return Response({"error": "Customer not found."}, status=404)



@api_view(['POST'])
@permission_classes([AllowAny])
def register_android_device(request):
    token = request.data.get('token')
    customer_id = request.data.get('customer_id') 
    mac_address = request.data.get('mac_address')  

    request_ip = request.META.get('REMOTE_ADDR', 'Unknown')
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

    logger.info("Android Device Registration: IP=%s | User-Agent=%s", request_ip, user_agent)
    logger.debug("Incoming data — token: %s, customer_id: %s, mac_address: %s", token, customer_id, mac_address)

    if not token or not customer_id or not mac_address: 
        logger.warning("Missing required fields: token=%s, customer_id=%s, mac_address=%s", token, customer_id, mac_address)
        return Response({"error": "Fields 'token', 'customer_id', and 'mac_address' are required."}, status=400)

    try:
        customer = AdminOutlet.objects.get(customer_id=customer_id)
        logger.info("Customer found: customer_id=%s", customer_id)

        try:
            device = AndroidDevice.objects.get(mac_address=mac_address, admin_outlet_id=customer.id)
            logger.info("Device found for mac_address=%s. Updating token.", mac_address)

            device.token = token
            device.admin_outlet = customer
            device.save()
        except AndroidDevice.DoesNotExist:
            logger.info("Device not found for mac_address=%s. Creating new device.", mac_address)

            device = AndroidDevice.objects.create(
                token=token,
                admin_outlet=customer,
                mac_address=mac_address
            )

        # Check mapping to vendor
        if hasattr(device, 'vendor') and device.vendor is not None:
            logger.info("Device is mapped to vendor: %s (ID: %s)", device.vendor.name, device.vendor.vendor_id)
            return Response({
                "status": "Device is mapped to vendor.",
                "mapped": True,
                "vendor_id": device.vendor.vendor_id,
                "vendor_name": device.vendor.name,
            }, status=200)
        else:
            logger.info("Device registered but not mapped to a vendor.")
            return Response({
                "status": "Device is registered but not yet mapped to a vendor.",
                "mapped": False,
                "vendor_id": None,
                "vendor_name": None,
            }, status=200)

    except AdminOutlet.DoesNotExist:
        logger.error("Customer not found for customer_id=%s", customer_id)
        return Response({"error": "Customer not found."}, status=404)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_android_apk(request):
    token = request.data.get('token')
    customer_id = request.data.get('customer_id') 
    mac_address = request.data.get('mac_address')  
    apk_version = request.data.get('apk_version') 

    request_ip = request.META.get('REMOTE_ADDR', 'Unknown')
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    logger.info("Android APK registration attempt from IP: %s | User-Agent: %s", request_ip, user_agent)
    logger.debug("Incoming data — token: %s, customer_id: %s, mac: %s, version: %s", token, customer_id, mac_address, apk_version)

    if not token or not customer_id or not mac_address or not apk_version:
        logger.warning("Missing fields: token=%s, customer_id=%s, mac_address=%s, apk_version=%s", token, customer_id, mac_address, apk_version)
        return Response({"error": "Fields 'token', 'customer_id', 'mac_address', and 'apk_version' are required."}, status=400) 

    try:
        # Validate customer
        admin_outlet = AdminOutlet.objects.get(customer_id=customer_id)
        logger.info("Validated customer: %s", customer_id)

        # Check if device exists by MAC
        device = AndroidAPK.objects.filter(mac_address=mac_address, admin_outlet=admin_outlet).first()

        if device:
            logger.info("Device already exists. Updating token and version for MAC: %s", mac_address)
            device.token = token
            device.apk_version = apk_version
            device.save()
        else:
            logger.info("New AndroidAPK device. Registering MAC: %s", mac_address)
            device = AndroidAPK.objects.create(
                token=token,
                mac_address=mac_address,
                apk_version=apk_version,
                admin_outlet=admin_outlet
            )

        # Check if mapped to a manager
        if device.user_profile:
            logger.info("Device is already mapped to manager: %s", device.user_profile.name)
            return Response({
                "status": "Device is mapped to a manager.",
                "mapped": True,
                "manager_id": device.user_profile.id,
                "manager_name": device.user_profile.name,
            }, status=200)
        else:
            logger.info("Device registered, not mapped to manager.")
            return Response({
                "status": "Device is registered but not yet mapped to a manager.",
                "mapped": False,
                "manager_id": None,
                "manager_name": None,
            }, status=200)

    except AdminOutlet.DoesNotExist:
        logger.error("Customer ID not found: %s", customer_id)
        return Response({"error": "Customer not found."}, status=404)


from firebase_admin import messaging
def send_firebase_admin_multicast(fcm_tokens, data_payload):
    """
    Sends a true Firebase Admin SDK multicast data+notification message to multiple devices.
    """

    if not fcm_tokens:
        logger.warning("No FCM tokens provided for multicast.")
        return False, {"error": "No tokens to send"}

    try:
        message = messaging.MulticastMessage(
            data={
                "type": "ready_orders",
                "orders": data_payload  # Ensure this is a string, if JSON dump is needed
            },
            notification=messaging.Notification(
                title="Order Ready!",
                body="Order Status Send to Android TV"
            ),
            tokens=fcm_tokens,
        )
        response = messaging.send_each_for_multicast(message)

        failed_tokens = []
        for idx, resp in enumerate(response.responses):
            if not resp.success:
                failed_tokens.append(fcm_tokens[idx])

        if failed_tokens:
            logger.warning(f"Multicast partially failed: {len(failed_tokens)} failed tokens.")
            return False, {"failed_tokens": failed_tokens}

        logger.info(f"FCM multicast successful: {response.success_count} sent.")
        return True, {"success_count": response.success_count}

    except Exception as e:
        logger.exception("Multicast FCM error")
        return False, {"error": str(e)}

# @api_view(['PATCH'])
# @permission_classes([AllowAny])
# def update_order(request):
#     try:
#         ip = request.META.get('HTTP_X_FORWARDED_FOR')
#         if ip:
#             ip = ip.split(',')[0] 
#         else:
#             ip = request.META.get('REMOTE_ADDR', 'Unknown')
#         request_ip = ip
#         user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

#         logger.info(f"Incoming PATCH /update_order API from IP: {request_ip}, User-Agent: {user_agent}")
#         logger.info(f"Request Data: {request.data}")
        
#         data = request.data
#         vendor_id = data.get('vendor_id')
#         token_no = data.get('token_no')
#         device_id = data.get('device_id')
#         counter_no = data.get('counter_no')
#         status_to_update = data.get('status', 'ready')

#         required_fields = ['vendor_id', 'token_no', 'device_id', 'counter_no', 'status']
#         missing_fields = [field for field in required_fields if not request.data.get(field)]
#         if missing_fields:
#             logger.warning(f"Missing required fields: {missing_fields}")
#             return Response(
#                 {"message": f"Missing fields: {', '.join(missing_fields)}"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Step 1: Fetch vendor and device
#         vendor = Vendor.objects.get(vendor_id=vendor_id)
#         device = Device.objects.get(serial_no=device_id,vendor_id=vendor.id)
        
#         logger.info(f"Vendor and Device resolved — Vendor Name: {vendor.name}, Device ID: {device.id}")

#         # Step 2: Send FCM notification with recent ready orders

#         android_devices = AndroidDevice.objects.filter(vendor=vendor)
        
#         fcm_tokens = list(android_devices.values_list('token', flat=True))
#         fcm_result = send_firebase_admin_multicast(fcm_tokens, json.dumps(data))
#         logger.info(f"FCM Multicast Result: {fcm_result}")

#         try:
#             # Try to fetch the existing order
#             order = Order.objects.get(token_no=token_no, vendor=vendor.id)
#             logger.info(f"Existing Order found — Updating status to {status_to_update}")
#             # Update the order's status and counter number
#             order.status = status_to_update
#             order.counter_no = counter_no
#             order.device = device
#             # Save the order
#             order.save()
#         except Order.DoesNotExist:
#             logger.info(f"No existing order found for token {token_no}. Creating a new order.")
#             # Order doesn't exist; create a new order with status "ready"
#             new_order_data = {
#                 'token_no': token_no,
#                 'vendor': vendor.id,
#                 'device': device.id,
#                 'counter_no': counter_no,
#                 'status': "ready"
#             }
#             serializer = OrdersSerializer(data=new_order_data)
#             if serializer.is_valid():
#                 logger.info(f"New Order created — Token: {token_no}, Vendor: {vendor.name}")
#                 order = serializer.save()
#             else:
#                 logger.error(f"Order serializer errors: {serializer.errors}")
#                 return Response(
#                     {"message": serializer.errors},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#         # Step 3: Send web push (if cooldown allows)
#         should_notify = (
#             status_to_update.lower() == "ready" and (
#                 not order.notified_at or
#                 (timezone.now() - order.notified_at) > timedelta(seconds=1)
#             )
#         )

#         push_errors = []
#         if should_notify:
#             vendor_serializer = VendorLogoSerializer(vendor, context={'request': request})
#             logo_url = vendor_serializer.data.get('logo_url', '')

#             payload = {
#                 "title": "Order Update",
#                 "body": f"Your order {token_no} is now ready.",
#                 "token_no": token_no,
#                 "status": status_to_update,
#                 "counter_no": counter_no,
#                 "name": vendor.name,
#                 "vendor_id": vendor.vendor_id,
#                 "location_id": vendor.location_id,
#                 "logo_url": logo_url,
#                 "type": "foodstatus"
#             }
            
#             logger.debug(f"Prepared push payload: {payload}")
            
#             subscriptions = PushSubscription.objects.filter(tokens__token_no=token_no,tokens__vendor=vendor).distinct()
            
#             logger.info(f"Found {subscriptions.count()} web push subscriptions to notify.")
            
#             for subscription in subscriptions:
#                 try:
#                     logger.debug(f"Sending web push to endpoint: {subscription.endpoint}")
#                     send_push_notification({
#                         "endpoint": subscription.endpoint,
#                         "keys": {
#                             "p256dh": subscription.p256dh,
#                             "auth": subscription.auth
#                         }
#                     }, payload)
#                 except Exception as e:
#                     logger.error(f"Error sending web push: {e}")
#                     push_errors.append(str(e))

#             # Step 4: Mark notified
#             order.notified_at = timezone.now()
#             order.save(update_fields=['notified_at'])
            
#             logger.info(f"Order {token_no} marked as notified at {order.notified_at}")

#         # Step 5: Final response
#         if push_errors:
#             return Response(
#                 {
#                     "message": "Order updated. FCM sent. Some web pushes failed.",
#                     "push_errors": push_errors
#                 },
#                 status=status.HTTP_207_MULTI_STATUS
#             )
            
#         logger.info(f"Order {token_no} update completed successfully with notifications.")
        
#         return Response(
#             {"message": "Order updated and notifications sent.", "token_no": token_no},
#             status=status.HTTP_200_OK
#         )

#     except Exception as e:
#         logger.exception("Exception occurred in update_order:")
#         return Response(
#             {"message": str(e)},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )
def get_vendor(vendor_id):
    return Vendor.objects.get(vendor_id=vendor_id)

def get_vendor_by_id(vendor_id):
    return Vendor.objects.get(id=vendor_id)

def get_device(device_id, vendor_id):
    return Device.objects.get(serial_no=device_id, vendor_id=vendor_id)

def get_order(token_no, vendor):
    return Order.objects.filter(token_no=token_no, vendor=vendor).first()
def create_or_update_order(token_no, vendor, device, counter_no, status):
    order = get_order(token_no, vendor)
    if order:
        logger.info(f"Updating existing order {token_no}")
        order.status = status
        order.counter_no = counter_no
        order.device = device
        order.save()
    else:
        logger.info(f"Creating new order {token_no}")
        order_data = {
            'token_no': token_no,
            'vendor': vendor.id,
            'device': device.id,
            'counter_no': counter_no,
            'status': status,
        }
        serializer = OrdersSerializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
    return order

# def create_or_update_order(token_no, vendor, device, counter_no, status,manager):
#     order = get_order(token_no, vendor)
#     if order:
#         logger.info(f"Updating existing order {token_no}")
#         order.status = status
#         order.counter_no = counter_no
#         order.device = device
#         order.user_profile = manager
#         order.save()
#     else:
#         logger.info(f"Creating new order {token_no}")
#         order_data = {
#             'token_no': token_no,
#             'vendor': vendor.id,
#             'device': device.id,
#             'counter_no': counter_no,
#             'status': status,
#             'manager': manager
#         }
#         serializer = OrdersSerializer(data=order_data)
#         serializer.is_valid(raise_exception=True)
#         order = serializer.save()
#     return order

def notify_fcm(vendor, data):
    android_devices = AndroidDevice.objects.filter(vendor=vendor)
    tokens = list(android_devices.values_list('token', flat=True))
    return send_firebase_admin_multicast(tokens, json.dumps(data))

PUSH_COOLDOWN_SECONDS = 1

@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_order(request):
    try:
        logger.info(f"PATCH /update_order from IP {request.META.get('REMOTE_ADDR')} — UA: {request.META.get('HTTP_USER_AGENT')}")
        
        data = request.data
        required_fields = ['vendor_id', 'token_no', 'device_id', 'counter_no', 'status']
        missing = [f for f in required_fields if not data.get(f)]
        
        if missing:
            logger.info(f"Missing fields: {', '.join(missing)}")
            return Response({"message": f"Missing fields: {', '.join(missing)}"}, status=status.HTTP_400_BAD_REQUEST)

        vendor = get_vendor(data['vendor_id'])
        device = get_device(data['device_id'], vendor.id)
        status_to_update = data['status']
        token_no = data['token_no']
        counter_no = data['counter_no']

        logger.info(f"Resolved Vendor: {vendor.name}, Device: {device.serial_no}, Token No: {token_no}, Counter No: {counter_no}, Status: {status_to_update}")

        # FCM Push
        fcm_result = notify_fcm(vendor, data)
        logger.info(f"FCM sent. Result: {fcm_result}")

        # Order Create or Update
        order = create_or_update_order(token_no, vendor, device, counter_no, status_to_update)

        push_errors = []
        if status_to_update.lower() == "ready" and (not order.notified_at or (timezone.now() - order.notified_at) > timedelta(seconds=PUSH_COOLDOWN_SECONDS)):
            vendor_serializer = VendorLogoSerializer(vendor, context={'request': request})
            payload = {
                "title": "Order Update",
                "body": f"Your order {token_no} is now ready.",
                "token_no": token_no,
                "status": status_to_update,
                "counter_no": counter_no,
                "name": vendor.name,
                "vendor_id": vendor.vendor_id,
                "location_id": vendor.location_id,
                "logo_url": vendor_serializer.data.get("logo_url", ""),
                "type": "foodstatus"
            }
            push_errors = notify_web_push(order, vendor, payload)
            order.notified_at = timezone.now()
            order.save(update_fields=['notified_at'])
            logger.info(f"Marked order {token_no} as notified.")

        response_msg = {"message": "Order updated and notifications sent.", "token_no": token_no}
        if push_errors:
            response_msg.update({"message": "Order updated. FCM sent. Some web pushes failed.", "push_errors": push_errors})
            return Response(response_msg, status=status.HTTP_207_MULTI_STATUS)

        return Response(response_msg, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception("Unhandled exception in update_order:")
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



