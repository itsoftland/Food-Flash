import json
import logging

from django.utils.timezone import now, localtime

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers

from .models import (Order, Vendor, Device,
                     AndroidDevice, PushSubscription,
                     AdminOutlet, AndroidAPK, UserProfile)

from .serializers import OrdersSerializer
from orders.serializers import VendorLogoSerializer
from .utils import send_push_notification, notify_web_push
from static.utils.functions.queries import get_order
from firebase_admin import messaging
from .mqtt_client import get_mqtt_config_for_vendor
from orders.utils import send_to_managers
from vendors.services.order_service import send_order_update
logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_current_time(request):
    current_ist = localtime(now())
    formatted_time = current_ist.strftime('%Y-%m-%d %H:%M:%S')
    return Response({'current_time': formatted_time})

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
    logger.debug("Incoming data — token=%s, customer_id=%s, mac_address=%s", token, customer_id, mac_address)

    # Validate required fields
    if not token or not customer_id or not mac_address:
        logger.warning("Missing required fields: token=%s, customer_id=%s, mac_address=%s", token, customer_id, mac_address)
        return Response(
            {"error": "Fields 'token', 'customer_id', and 'mac_address' are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        customer = AdminOutlet.objects.get(customer_id=customer_id)
        logger.info("Customer found: customer_id=%s (AdminOutlet ID: %s)", customer_id, customer.id)
    except AdminOutlet.DoesNotExist:
        logger.error("Customer not found: customer_id=%s", customer_id)
        return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

    # Register or update device
    try:
        device, created = AndroidDevice.objects.get_or_create(
            mac_address=mac_address,
            admin_outlet=customer,
            defaults={'token': token}
        )
        if not created:
            logger.info("Device found for mac_address=%s. Updating token.", mac_address)
            device.token = token
            device.save()
        else:
            logger.info("New device created: mac_address=%s, token=%s", mac_address, token)
    except Exception as e:
        logger.error("Failed to register/update device: %s", str(e), exc_info=True)
        return Response({"error": "Failed to register/update device."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Check vendor mapping
    if hasattr(device, 'vendor') and device.vendor:
        logger.info("Device mapped to vendor: %s (ID: %s)", device.vendor.name, device.vendor.vendor_id)
        return Response({
            "status": "Device is mapped to vendor.",
            "mapped": True,
            "vendor_id": device.vendor.vendor_id,
            "vendor_name": device.vendor.name,
            "mqtt_config": get_mqtt_config_for_vendor(device.vendor, device)
        }, status=status.HTTP_200_OK)

    logger.info("Device registered but not mapped to any vendor.")
    return Response({
        "status": "Device is registered but not yet mapped to a vendor.",
        "mapped": False,
        "vendor_id": None,
        "vendor_name": None,
        "mqtt_config": None
    }, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_android_device(request):
#     token = request.data.get('token')
#     customer_id = request.data.get('customer_id') 
#     mac_address = request.data.get('mac_address')  

#     request_ip = request.META.get('REMOTE_ADDR', 'Unknown')
#     user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

#     logger.info("Android Device Registration: IP=%s | User-Agent=%s", request_ip, user_agent)
#     logger.debug("Incoming data — token: %s, customer_id: %s, mac_address: %s", token, customer_id, mac_address)

#     if not token or not customer_id or not mac_address: 
#         logger.warning("Missing required fields: token=%s, customer_id=%s, mac_address=%s", token, customer_id, mac_address)
#         return Response({"error": "Fields 'token', 'customer_id', and 'mac_address' are required."}, status=400)

#     try:
#         customer = AdminOutlet.objects.get(customer_id=customer_id)
#         logger.info("Customer found: customer_id=%s", customer_id)

#         try:
#             device = AndroidDevice.objects.get(mac_address=mac_address, admin_outlet_id=customer.id)
#             logger.info("Device found for mac_address=%s. Updating token.", mac_address)

#             device.token = token
#             device.admin_outlet = customer
#             device.save()
#         except AndroidDevice.DoesNotExist:
#             logger.info("Device not found for mac_address=%s. Creating new device.", mac_address)

#             device = AndroidDevice.objects.create(
#                 token=token,
#                 admin_outlet=customer,
#                 mac_address=mac_address
#             )

#         # Check mapping to vendor
#         if hasattr(device, 'vendor') and device.vendor is not None:
#             logger.info("Device is mapped to vendor: %s (ID: %s)", device.vendor.name, device.vendor.vendor_id)

#             return Response({
#                 "status": "Device is mapped to vendor.",
#                 "mapped": True,
#                 "vendor_id": device.vendor.vendor_id,
#                 "vendor_name": device.vendor.name,
#                 "mqtt_config": get_mqtt_config_for_vendor(device.vendor,device)
#             }, status=200)

#         else:
#             logger.info("Device registered but not mapped to a vendor.")
#             return Response({
#                 "status": "Device is registered but not yet mapped to a vendor.",
#                 "mapped": False,
#                 "vendor_id": None,
#                 "vendor_name": None,
#                 "mqtt_config": None
#             }, status=200)

#     except AdminOutlet.DoesNotExist:
#         logger.error("Customer not found for customer_id=%s", customer_id)
#         return Response({"error": "Customer not found."}, status=404)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_android_apk(request):
#     token = request.data.get('token')
#     customer_id = request.data.get('customer_id') 
#     mac_address = request.data.get('mac_address')  
#     apk_version = request.data.get('apk_version') 

#     request_ip = request.META.get('REMOTE_ADDR', 'Unknown')
#     user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
#     logger.info("Android APK registration attempt from IP: %s | User-Agent: %s", request_ip, user_agent)
#     logger.debug("Incoming data — token: %s, customer_id: %s, mac: %s, version: %s", token, customer_id, mac_address, apk_version)

#     if not token or not customer_id or not mac_address or not apk_version:
#         logger.warning("Missing fields: token=%s, customer_id=%s, mac_address=%s, apk_version=%s", token, customer_id, mac_address, apk_version)
#         return Response({"error": "Fields 'token', 'customer_id', 'mac_address', and 'apk_version' are required."}, status=400) 

#     try:
#         # Validate customer
#         admin_outlet = AdminOutlet.objects.get(customer_id=customer_id)
#         logger.info("Validated customer: %s", customer_id)

#         # Check if device exists by MAC
#         device = AndroidAPK.objects.filter(mac_address=mac_address, admin_outlet=admin_outlet).first()

#         if device:
#             logger.info("Device already exists. Updating token and version for MAC: %s", mac_address)
#             device.token = token
#             device.apk_version = apk_version
#             device.save()
#         else:
#             logger.info("New AndroidAPK device. Registering MAC: %s", mac_address)
#             device = AndroidAPK.objects.create(
#                 token=token,
#                 mac_address=mac_address,
#                 apk_version=apk_version,
#                 admin_outlet=admin_outlet
#             )

#         # Check if mapped to a manager
#         if device.user_profile:
#             logger.info("Device is already mapped to manager: %s", device.user_profile.name)
#             return Response({
#                 "status": "Device is mapped to a manager.",
#                 "mapped": True,
#                 "manager_id": device.user_profile.id,
#                 "manager_name": device.user_profile.name,
#             }, status=200)
#         else:
#             logger.info("Device registered, not mapped to manager.")
#             return Response({
#                 "status": "Device is registered but not yet mapped to a manager.",
#                 "mapped": False,
#                 "manager_id": None,
#                 "manager_name": None,
#             }, status=200)

#     except AdminOutlet.DoesNotExist:
#         logger.error("Customer ID not found: %s", customer_id)
#         return Response({"error": "Customer not found."}, status=404)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_android_apk(request):
    """
    Registers or updates an Android APK device for a customer.
    - Validates customer and optional manager_id.
    - Updates or creates the AndroidAPK record.
    - Returns mapping status with manager if available.
    """
    token = request.data.get('token')
    customer_id = request.data.get('customer_id')
    mac_address = request.data.get('mac_address')
    apk_version = request.data.get('apk_version')
    manager_id = request.data.get('manager_id')

    logger.debug(
        "[register_android_apk] Incoming data — token=%s, customer_id=%s, mac=%s, version=%s, manager_id=%s",
        token, customer_id, mac_address, apk_version, manager_id
    )

    # === Step 1: Validate Required Fields ===
    if not token or not customer_id or not mac_address or not apk_version:
        logger.warning(
            "[register_android_apk] Missing required fields — token=%s, customer_id=%s, mac=%s, apk_version=%s",
            token, customer_id, mac_address, apk_version
        )
        return Response(
            {"error": "Fields 'token', 'customer_id', 'mac_address', and 'apk_version' are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # === Step 2: Validate Customer ===
        admin_outlet = AdminOutlet.objects.get(customer_id=customer_id)
        logger.info("[register_android_apk] Validated customer_id=%s", customer_id)

        user_profile = None
        # === Step 3: Validate Manager if Provided ===
        if manager_id:
            try:
                user_profile = UserProfile.objects.get(
                    id=manager_id,
                    role__in=['outlet_manager', 'admin_manager', 'order_manager'],
                    admin_outlet=admin_outlet
                )
                logger.info("[register_android_apk] Validated manager_id=%s for customer_id=%s", manager_id, customer_id)
            except UserProfile.DoesNotExist:
                logger.warning("[register_android_apk] Invalid manager_id=%s for customer_id=%s", manager_id, customer_id)
                return Response({"error": "Invalid manager ID for this customer."}, status=status.HTTP_400_BAD_REQUEST)

        # === Step 4: Check Device by MAC and Manager ===
        device = AndroidAPK.objects.filter(
            mac_address=mac_address,
            admin_outlet=admin_outlet,
            user_profile=user_profile if user_profile else None
        ).first()
        if device:
            logger.info(
                "[register_android_apk] Device already exists. Updating token and version — MAC=%s, manager=%s",
                mac_address, user_profile.name if user_profile else "None"
            )
            device.token = token
            device.apk_version = apk_version
            if user_profile:
                device.user_profile = user_profile
            device.save()
        else:
            logger.info("[register_android_apk] Registering new device — MAC=%s", mac_address)
            device = AndroidAPK.objects.create(
                token=token,
                mac_address=mac_address,
                apk_version=apk_version,
                admin_outlet=admin_outlet,
                user_profile=user_profile
            )

        # === Step 5: Return Mapping Status ===
        if device.user_profile:
            logger.info(
                "[register_android_apk] Device mapped to manager_id=%s (%s)",
                device.user_profile.id, device.user_profile.name
            )
            return Response({
                "status": "Device is mapped to a manager.",
                "mapped": True,
                "manager_id": device.user_profile.id,
                "manager_name": device.user_profile.name,
            }, status=status.HTTP_200_OK)

        logger.info("[register_android_apk] Device registered but not mapped to any manager.")
        return Response({
            "status": "Device is registered but not yet mapped to a manager.",
            "mapped": False,
            "manager_id": None,
            "manager_name": None,
        }, status=status.HTTP_200_OK)

    except AdminOutlet.DoesNotExist:
        logger.error("[register_android_apk] Customer ID not found: %s", customer_id)
        return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.exception("[register_android_apk] Unexpected error: %s", str(e))
        return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    
def get_vendor(vendor_id):
    return Vendor.objects.get(vendor_id=vendor_id)

def get_device(device_id, vendor_id):
    return Device.objects.get(serial_no=device_id, vendor_id=vendor_id)


def create_or_update_order(token_no, vendor, device, counter_no, status):
    order = get_order(token_no, vendor)
    if order:
        logger.info(f"Updating existing order {token_no}")
        order.status = status
        order.counter_no = counter_no
        order.device = device
        order.updated_by = "keypad_device"
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
        if not serializer.is_valid():
            logger.error(f"Order creation failed: {serializer.errors}")
            raise serializers.ValidationError(serializer.errors)
        order = serializer.save()
    return order

def notify_fcm(vendor, data):
    android_devices = AndroidDevice.objects.filter(vendor=vendor)
    tokens = list(android_devices.values_list('token', flat=True))
    return send_firebase_admin_multicast(tokens, json.dumps(data))

PUSH_COOLDOWN_SECONDS = 2

@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_order(request):
    try:
        logger.info(
            f"[update_order] PATCH request from IP={request.META.get('REMOTE_ADDR')} "
            f"UA={request.META.get('HTTP_USER_AGENT')}"
        )
        
        # Validate request data
        data = request.data
        required_fields = ['vendor_id', 'token_no', 'device_id', 'counter_no', 'status']
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            logger.warning(f"[update_order] Missing fields: {', '.join(missing)}")
            return Response(
                {"message": f"Missing fields: {', '.join(missing)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get vendor and device
        try:
            vendor = get_vendor(data['vendor_id'])
        except Vendor.DoesNotExist:
            logger.warning(f"[update_order] Vendor not found: vendor_id={data['vendor_id']}")
            return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            device = get_device(data['device_id'], vendor.id)
        except Device.DoesNotExist:
            logger.warning(
                f"[update_order] Device not found: device_id={data['device_id']} vendor_id={vendor.id}"
            )
            return Response({"message": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        status_to_update = data['status']
        token_no = data['token_no']
        counter_no = data['counter_no']

        logger.info(
            f"[update_order] Resolved: vendor={vendor.name} device={device.serial_no} "
            f"token_no={token_no} counter_no={counter_no} status={status_to_update}"
        )
        
        # FCM push notifications if TV communication mode is not MQTT
        if vendor.config.tv_communication_mode != "MQTT":
            try:
                fcm_result = notify_fcm(vendor, data)
                logger.info(f"[update_order] FCM sent successfully: {fcm_result}")
            except Exception as e:
                logger.exception("[update_order] FCM sending failed")
                fcm_result = {"error": str(e)}
        
        # Create or update order in DB
        order = create_or_update_order(token_no, vendor, device, counter_no, status_to_update)
        logger.info(f"[update_order] Order {order.id} created/updated for token_no={token_no}")
        
        # MQTT Publish
        logger.info(f"[update_order] Sending MQTT update for vendor {vendor.vendor_id}, token {token_no}")
        
        if not hasattr(vendor, 'config') or not vendor.config.mqtt_mode:
            logger.warning(f"[update_order] Vendor {vendor.vendor_id} has no MQTT configuration")
            return Response(
                {"message": "Vendor has no MQTT configuration."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            mqtt = send_order_update(vendor)
            if mqtt:
                logger.info(f"[update_order] ✅ MQTT update sent successfully for vendor {vendor.vendor_id}")
            else:
                logger.error(f"[update_order] ❌ Failed to send MQTT update for vendor {vendor.vendor_id}")
                return Response(
                    {"message": "Failed to send MQTT update."}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Exception as mqtt_err:
            logger.exception(f"[update_order] MQTT publish failed: {mqtt_err}")
            return Response(
                {"message": "MQTT publish failed."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Web push notifications if status is "ready"
        push_errors = []
        if status_to_update.lower() == "ready" and (
            not order.notified_at or (now() - order.notified_at).total_seconds() > PUSH_COOLDOWN_SECONDS
        ):
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

            # Notify managers via FCM
            send_to_managers(vendor, payload)
            
            try:
                push_errors = notify_web_push(order, vendor, payload)
            except Exception as push_err:
                logger.error(f"[update_order] Web push failed: {push_err}")
                push_errors = [str(push_err)]
            
            logger.info(f"[update_order] Web push notifications sent. Errors: {push_errors}")
            order.notified_at = now()
            order.save(update_fields=['notified_at'])
            logger.info(f"[update_order] Marked order {token_no} as notified at {order.notified_at}")

        response_msg = {
            "message": "Order updated and notifications sent.",
            "token_no": token_no
        }
        logger.info(f"[update_order] Completed successfully for token {token_no}")
        return Response(response_msg, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception(f"[update_order] Unexpected error: {e}")
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
