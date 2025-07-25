import logging
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from vendors.models import (Order, Vendor, UserProfile,
                            ChatMessage)
from vendors.serializers import OrdersSerializer
from vendors.utils import notify_web_push

from orders.serializers import VendorLogoSerializer
from .serializers import ChatMessageSerializer  

from static.utils.functions.utils import get_filtered_date_range
from static.utils.functions.queries import update_existing_order_by_manager
from static.utils.functions.notifications import notify_android_tv

logger = logging.getLogger(__name__)


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_by_manager(request):
    token_no = request.data.get('token_no')
    vendor_id = request.data.get('vendor_id')
    manager_id = request.data.get('manager_id')  

    # Validate inputs
    if not token_no or not vendor_id or not manager_id:
        return Response({'error': 'token_no, vendor_id, and manager_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token_no = int(token_no)
        vendor_id = int(vendor_id)
        manager_id = int(manager_id)
    except ValueError:
        return Response({'error': 'All fields must be valid integers.'}, status=status.HTTP_400_BAD_REQUEST)
    vendor = Vendor.objects.get(id=vendor_id)
    # Dynamically build the base URL
    base_url = request.build_absolute_uri('/')  
    # Build the tracking URL (assuming 'home/' is always part of it)
    tracking_url = f"{base_url}home/?location_id={vendor.location_id}&vendor_id={vendor.vendor_id}&token_no={token_no}"

    # Check if order already exists
    try:
        order = Order.objects.get(token_no=token_no, vendor__id=vendor_id)
        
        return Response({
            'message': 'Order already exists for this token number.',
            'id': order.id,
            'token_no': order.token_no,
            'counter_no': order.counter_no,
            'updated_by': order.updated_by,
            'tracking_url': tracking_url,
            'status': order.status,
            'vendor': order.vendor.id,
            'name': order.vendor.name,
            'vendor_name': order.vendor.name,
            'manager_id': order.user_profile.id if order.user_profile else None,
            'manager_name': order.user_profile.name if order.user_profile else None,
            'device': order.device.id if order.device else None,
            'shown_on_tv': order.shown_on_tv,
            'notified_at': order.notified_at,
            'created_at': order.created_at,
            'updated_at': order.updated_at,
        }, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        pass

    # Create new order
    try:
        manager = UserProfile.objects.filter(id=manager_id).first()

        new_order_data = {
            'name': vendor.name,
            'token_no': token_no,
            'vendor': vendor.id,
            'location_id': vendor.location_id,
            'counter_no': 1,
            'device': None,
            'updated_by': 'manager',
            'status': 'created',
            'type': 'foodstatus',
            'manager_id': manager.id
        }

        serializer = OrdersSerializer(data=new_order_data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            # Add tracking URL to the response data
            data['tracking_url'] = tracking_url
            data['message'] = 'Order created successfully by manager.'
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_today_orders(request):
    try:
        vendor_id = request.GET.get('vendor_id')
        if not vendor_id:
            return Response({"error": "vendor_id required"}, status=400)

        # Use your utility to get start and end of "today"
        start_dt, end_dt = get_filtered_date_range('today')

        if not start_dt or not end_dt:
            return Response({"error": "Invalid date range"}, status=400)

        # Filter orders created today
        todays_orders = Order.objects.filter(
            vendor__id=vendor_id,
            created_at__range=(start_dt, end_dt)
        ).order_by('-updated_at')

        data = OrdersSerializer(todays_orders, many=True, context={'request': request}).data
        return Response({
            "message": "Today's orders retrieved successfully.",
            "count": len(data),
            "detail":data,
            }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
from django.conf import settings

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def manager_order_update(request):
    try:
        logger.info("📥 PATCH /update_order")
        logger.info(f"IP: {request.META.get('REMOTE_ADDR')}, UA: {request.META.get('HTTP_USER_AGENT')}")
        logger.debug(f"Request Data: {request.data}")

        data = request.data
        required_fields = ['token_no', 'status']
        missing = [f for f in required_fields if f not in data or data[f] in [None, ""]]

        if missing:
            logger.warning(f"⛔ Missing fields: {', '.join(missing)}")
            return Response({"message": f"Missing fields: {', '.join(missing)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate token_no as int
        try:
            token_no = int(data['token_no'])
        except (TypeError, ValueError):
            logger.warning("❌ token_no must be a valid integer.")
            return Response({"message": "token_no must be a valid integer."}, status=status.HTTP_400_BAD_REQUEST)

        status_to_update = data['status']

        # Validate manager
        manager = getattr(request.user, 'profile_roles', None)
        if not manager or not manager.exists():
            logger.warning("⚠️ No manager profile found for the user.")
            return Response({"message": "User is not a manager."}, status=status.HTTP_403_FORBIDDEN)

        manager = manager.first()
        if not manager.vendor:
            logger.warning("⚠️ Manager does not have an associated vendor.")
            return Response({"message": "Manager does not have an associated vendor."}, status=status.HTTP_403_FORBIDDEN)

        vendor = manager.vendor
        logger.info(f"🔧 Manager: {manager.name}, Vendor: {vendor.name} ({vendor.vendor_id}), Token: {token_no}, Status: {status_to_update}")

        order = Order.objects.filter(token_no=token_no, vendor=vendor, created_date=timezone.now().date()).first()
        if not order:
            logger.warning(f"❌ No order found for token_no {token_no} today.")
            return Response({"message": f"Order with token_no {token_no} not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize vendor logo
        vendor_serializer = VendorLogoSerializer(vendor, context={'request': request})
        logo_url = vendor_serializer.data.get("logo_url", "")
        if status_to_update.lower() == "ready":
            body = f"Your order {token_no} status: {status_to_update.capitalize()}"
        else:
            body = f"Your order {token_no} has an update from the manager."


        # Prepare common push payload
        payload = {
            "title": "Order Update by Manager",
            "body": body,
            "token_no": token_no,
            "status": status_to_update.lower(),
            "counter_no": order.counter_no,
            "name": vendor.name,
            "vendor_id": vendor.vendor_id,
            "location_id": vendor.location_id,
            "logo_url": logo_url,
            "type": "foodstatus" if status_to_update == "ready" else "manager",
            "message_id":None
        }

        android_tv_success = None
        android_tv_info = None
        push_errors = []

        # ✅ IF status is "ready"
        if status_to_update.lower() == "ready":
            # 1. Notify Android TV
            android_tv_success, android_tv_info = notify_android_tv(vendor, data)
            logger.info(f"📺 Android TV FCM sent | Success: {android_tv_success} | Info: {android_tv_info}")

            # 2. Update in DB
            device = None  # Not a customer device
            updated_order = update_existing_order_by_manager(token_no, vendor, device, status_to_update, manager)
            if not updated_order:
                logger.warning(f"❌ Failed to update order {token_no}")
                return Response({"message": "Order update failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info(f"✅ Order {updated_order.id} updated to status: {status_to_update}")

            # 3. Send Web Push (only if cooldown passed)
            cooldown = getattr(settings, "PUSH_COOLDOWN_SECONDS", 5)
            if not order.notified_at or (timezone.now() - order.notified_at) > timedelta(seconds=cooldown):
                logger.info(f"📤 Sending web push...")
                push_errors = notify_web_push(order, vendor, payload)
                order.notified_at = timezone.now()
                order.save(update_fields=["notified_at"])
                logger.info(f"🕒 Order {token_no} marked as notified at {order.notified_at}")
            else:
                logger.info(f"⏳ Cooldown active. Skipping web push for {token_no}.")

        # ⚠️ IF status is NOT "ready"
        else:
            MAX_MESSAGE_LENGTH = 200

            if status_to_update and len(status_to_update) > MAX_MESSAGE_LENGTH:
                return Response(
                    {"error": f"Message too long. Limit is {MAX_MESSAGE_LENGTH} characters."},
                    status=400
                )
            logger.info("ℹ️ Status not 'ready' — skipping DB and Android TV. Sending web push with type 'manager'.")
            # 1. Save chat message first with is_send=True (optimistic approach)
            chat_message = ChatMessage.objects.create(
                vendor=vendor,
                token_no=token_no,
                created_date=timezone.now().date(),
                sender='manager',
                is_send=True,
                message_text=status_to_update
            )

            # 2. Add message ID to payload
            payload["message_id"] = chat_message.id

            # 3. Try sending the web push
            push_errors = notify_web_push(order, vendor, payload)

            if not push_errors:
                logger.info(f"📤 Web push sent successfully for {token_no}")
            else:
                error_messages = "\n".join(
                    f"{error.__class__.__name__}: {str(error)}" for error in push_errors
                )
                logger.warning(f"❌ Failed to send web push for {token_no}. Errors:\n{error_messages}")

                # 4. Update the ChatMessage to is_send=False since push failed
                chat_message.is_send = False
                chat_message.save(update_fields=["is_send"])



        # 📦 Final response
        return Response({
            "success": True,
            "message": f"Order {'updated and ' if status_to_update == 'ready' else ''}notified successfully.",
            "token_no": token_no,
            "android_tv": android_tv_success,
            "android_tv_info": android_tv_info,
            "web_push": not push_errors,
            "web_push_info": push_errors
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception("🔥 Unhandled exception in manager_order_update:")
        return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_history(request):
    vendor_id = request.GET.get('vendor_id')
    token_no = request.GET.get('token_no')

    # Validate input
    if not vendor_id or not token_no:
        return Response({"error": "vendor_id and token_no are required."}, status=400)

    try:
        vendor = Vendor.objects.get(id=int(vendor_id))
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found."}, status=404)

    try:
        token_no = int(token_no)
    except ValueError:
        return Response({"error": "Invalid token_no."}, status=400)

    messages = ChatMessage.objects.filter(
        vendor=vendor,
        token_no=token_no,
        created_date=timezone.now().date()
    ).order_by('created_at')
    # ✅ Mark only user messages as read
    ChatMessage.objects.filter(
        vendor=vendor,
        token_no=token_no,
        created_date=timezone.now().date(),
        sender='user',
        is_read=False
    ).update(is_read=True)

    serializer = ChatMessageSerializer(messages, many=True)
    return Response({"messages": serializer.data}, status=200)
