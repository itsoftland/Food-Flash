import logging
import json
import random
from datetime import timedelta
import pytz
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from .models import Order, Vendor, Device, AndroidDevice, PushSubscription, AdminOutlet
from .serializers import OrdersSerializer
from orders.serializers import VendorLogoSerializer
from .utils import send_push_notification

SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

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

@login_required
def company_dashboard(request):
    try:
        admin_outlet = request.user.admin_outlet  # access related AdminOutlet instance
    except AdminOutlet.DoesNotExist:
        return redirect('/login')

    context = {
        'admin_outlet': admin_outlet
    }
    return render(request, 'orders/company/company_dashboard.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # or whatever your dashboard URL is
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

@api_view(['POST'])
@permission_classes([AllowAny])
def register_device(request):
    serial_no = request.data.get('serial_no')
    customer_id = request.data.get('customer_id')

    if not serial_no or not customer_id:
        return Response({"error": "Fields 'serial_no' and 'customer_id' are required."}, status=400)

    try:
        # Step 1: Validate customer
        customer = AdminOutlet.objects.get(customer_id=customer_id)
        
        try:
            # Step 2: Check if device exists with this serial_no
            existing_device = Device.objects.get(serial_no=serial_no)

            if existing_device.admin_outlet == customer:
                # Same customer and same serial — already registered
                if existing_device.vendor is not None:
                    return Response({
                        "status": "Device is already registered and mapped to vendor.",
                        "mapped": True,
                        "vendor_id": existing_device.vendor.vendor_id,
                        "vendor_name": existing_device.vendor.name,
                    }, status=200)
                else:
                    return Response({
                        "status": "Device is already registered but not yet mapped to a vendor.",
                        "mapped": False,
                        "vendor_id": None,
                        "vendor_name": None,
                    }, status=200)
            else:
                # Serial exists but with a different customer
                return Response({
                    "error": "Serial number already registered with another customer."
                }, status=409)

        except Device.DoesNotExist:
            # Step 4: New device, create
            device = Device.objects.create(
                serial_no=serial_no,
                admin_outlet=customer,
                vendor=None  # vendor can be assigned later
            )
            return Response({
                "status": "Device is registered but not yet mapped to a vendor.",
                "mapped": False,
                "vendor_id": None,
                "vendor_name": None,
            }, status=201)

    except AdminOutlet.DoesNotExist:
        return Response({"error": "Customer not found."}, status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_android_device(request):
    token = request.data.get('token')
    customer_id = request.data.get('customer_id') 
    mac_address = request.data.get('mac_address')  

    if not token or not customer_id or not mac_address: 
        return Response({"error": "Fields 'token', 'customer_id', and 'mac_address' are required."}, status=400)

    try:
        customer = AdminOutlet.objects.get(customer_id=customer_id)

        # Check if a device with the mac_address exists
        try:
            device = AndroidDevice.objects.get(mac_address=mac_address)
            # If exists, update the token and customer
            device.token = token
            device.admin_outlet = customer
            device.save()
        except AndroidDevice.DoesNotExist:
            # If not exists, create a new device entry
            device = AndroidDevice.objects.create(
                token=token,
                admin_outlet=customer,
                mac_address=mac_address
            )

        # Check if the device is mapped to a vendor
        if hasattr(device, 'vendor') and device.vendor is not None:
            return Response({
                "status": "Device is mapped to vendor.",
                "mapped": True,
                "vendor_id": device.vendor.vendor_id,
                "vendor_name": device.vendor.name,
            }, status=200)
        else:
            return Response({
                "status": "Device is registered but not yet mapped to a vendor.",
                "mapped": False,
                "vendor_id": None,
                "vendor_name": None,
            }, status=200)

    except AdminOutlet.DoesNotExist:
        return Response({"error": "Customer not found."}, status=404)

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        settings.FIREBASE_SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )
    credentials.refresh(Request())
    return credentials.token

def send_fcm_data_message(fcm_token, data_payload):
    """
    Sends a Firebase Cloud Messaging (FCM) data message with a given payload.
    """
    access_token = get_access_token()
    url = f'https://fcm.googleapis.com/v1/projects/{settings.FIREBASE_PROJECT_ID}/messages:send'

    message = {
        "message": {
            "token": fcm_token,
            "data": {
                "type": "ready_orders",
                "orders": json.dumps(data_payload)
            },
            "notification": {
                "title": "Order Ready!",
                "body": "Your food is ready for pickup."
            },
            "android": {
                "priority": "high"
            }
        }
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; UTF-8',
    }

    response = requests.post(url, headers=headers, json=message)
    return response.status_code == 200, response.json()

#sending payload directly and use firebase cloud messaging
@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_order(request):
    try:
        data = request.data
        vendor_id = data.get('vendor_id')
        token_no = data.get('token_no')
        device_id = data.get('device_id')
        counter_no = data.get('counter_no')
        status_to_update = data.get('status', 'ready')

        if not all([vendor_id, token_no, device_id, counter_no, status_to_update]):
            return Response(
                {"message": "All fields vendor_id, token_no, device_id, counter_no, and status are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        logger.info(f"Update Order Request Received: token_no={token_no}, vendor_id={vendor_id}, device_id={device_id}, counter_no={counter_no}, status={status_to_update}")
        # Step 1: Fetch vendor and device
        vendor = Vendor.objects.get(vendor_id=vendor_id)
        device = Device.objects.get(serial_no=device_id)

        # Step 2: Send FCM notification with recent ready orders

        android_devices = AndroidDevice.objects.filter(vendor=vendor)
        for devices in android_devices:
            send_fcm_data_message(devices.token, data)


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
                'device': device.id,
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

        # Step 3: Send web push (if cooldown allows)
        should_notify = (
            status_to_update.lower() == "ready" and (
                not order.notified_at or
                (timezone.now() - order.notified_at) > timedelta(minutes=1)
            )
        )

        push_errors = []
        if should_notify:
            vendor_serializer = VendorLogoSerializer(vendor, context={'request': request})
            logo_url = vendor_serializer.data.get('logo_url', '')

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

            subscriptions = PushSubscription.objects.filter(tokens__token_no=token_no,tokens__vendor=vendor).distinct()
            for subscription in subscriptions:
                try:
                    send_push_notification({
                        "endpoint": subscription.endpoint,
                        "keys": {
                            "p256dh": subscription.p256dh,
                            "auth": subscription.auth
                        }
                    }, payload)
                except Exception as e:
                    push_errors.append(str(e))

            # Step 4: Mark notified
            order.notified_at = timezone.now()
            order.save(update_fields=['notified_at'])

        # Step 5: Final response
        if push_errors:
            return Response(
                {
                    "message": "Order updated. FCM sent. Some web pushes failed.",
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

def generate_unique_vendor_id():
    while True:
        # Generate a random 6-digit number, first digit 1-9
        vendor_id = random.randint(100000, 999999)
        if not Vendor.objects.filter(vendor_id=vendor_id).exists():
            return vendor_id

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def create_vendor(request):
    try:
        admin_outlet_id = request.data.get('admin_outlet')
        admin_outlet = get_object_or_404(AdminOutlet, id=admin_outlet_id)

        name = request.data.get('name')
        location = request.data.get('location')
        place_id = request.data.get('place_id', '')
        location_id = request.data.get('location_id')
        
        # Generate unique vendor_id
        vendor_id = generate_unique_vendor_id()
        
        # Handle logo file upload (store filename only)
        logo_file = request.FILES.get('logo')
        logo_path = None
        if logo_file:
            logo_path = default_storage.save('vendor_logos/' + logo_file.name, ContentFile(logo_file.read()))

        # Handle multiple menu files upload
        menu_files = request.FILES.getlist('menu_files')
        menu_paths = []
        for file in menu_files:
            path = default_storage.save('menus/' + file.name, ContentFile(file.read()))
            menu_paths.append(path)

        # Create Vendor instance
        vendor = Vendor.objects.create(
            admin_outlet=admin_outlet,
            name=name,
            location=location,
            place_id=place_id,
            vendor_id=vendor_id,
            location_id=location_id,
            logo=logo_path,
            menus=json.dumps(menu_paths),
        )
        # Assign Device by serial_no if provided
        device_mapping_serial = request.data.get('device_mapping')
        if device_mapping_serial:
            try:
                device = Device.objects.get(serial_no=device_mapping_serial)
                device.vendor = vendor
                device.save()
            except Device.DoesNotExist:
                # You may log this or return a warning in response if needed
                pass

        # Assign AndroidDevice by mac_address if provided
        tv_mapping_mac = request.data.get('tv_mapping')
        if tv_mapping_mac:
            try:
                android_device = AndroidDevice.objects.get(mac_address=tv_mapping_mac)
                android_device.vendor = vendor
                android_device.save()
            except AndroidDevice.DoesNotExist:
                # You may log this or return a warning in response if needed
                pass

        return Response({
            'success': True,
            'message': 'Vendor created successfully.',
            'vendor_id': vendor.vendor_id,
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

