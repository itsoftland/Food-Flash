import logging
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from vendors.models import Order, Vendor, UserProfile
from vendors.serializers import OrdersSerializer
from vendors.utils import notify_web_push

from orders.serializers import VendorLogoSerializer

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

# @api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
# def manager_order_update(request):
#     try:
#         logger.info("📥 PATCH /update_order")
#         logger.info(f"IP: {request.META.get('REMOTE_ADDR')}, UA: {request.META.get('HTTP_USER_AGENT')}")
#         logger.debug(f"Request Data: {request.data}")

#         data = request.data
#         required_fields = ['token_no', 'status']
#         missing = [f for f in required_fields if f not in data or data[f] in [None, ""]]


#         if missing:
#             logger.warning(f"⛔ Missing fields: {', '.join(missing)}")
#             return Response({"message": f"Missing fields: {', '.join(missing)}"}, status=status.HTTP_400_BAD_REQUEST)

#         manager = getattr(request.user, 'profile_roles', None)
#         if not manager or not manager.exists():
#             logger.warning("⚠️ No manager profile found for the user.")
#             return Response({"message": "User is not a manager."}, status=status.HTTP_403_FORBIDDEN)

#         manager = manager.first()
#         if not manager.vendor:
#             logger.warning("⚠️ Manager does not have an associated vendor.")
#             return Response({"message": "Manager does not have an associated vendor."}, status=status.HTTP_403_FORBIDDEN)
        
#         vendor = manager.vendor
#         token_no = data['token_no']
#         status_to_update = data['status']
#         device = None  # ensure no device association

#         logger.info(f"🔧 Manager: {manager.name}, Vendor: {vendor.name} ({vendor.vendor_id}), Token: {token_no}, Status: {status_to_update}")

#         # Attempt order update
#         order = update_existing_order_by_manager(token_no, vendor, device, status_to_update, manager)
#         if not order:
#             logger.warning(f"❌ No order found with token_no: {token_no} for vendor {vendor.name}")
#             return Response({"message": f"Order with token_no {token_no} not found."}, status=status.HTTP_404_NOT_FOUND)

#         logger.info(f"✅ Order found and updated: {order.id} — new status: {status_to_update}")

#         # Android TV push
#         fcm_result = notify_android_tv(vendor, data)
#         logger.info(f"📺 Android TV FCM sent | Result: {fcm_result}")

#         push_errors = []
#         if status_to_update.lower() == "ready":
#             from django.conf import settings
#             cooldown = getattr(settings, "PUSH_COOLDOWN_SECONDS", 5)

#             if not order.notified_at or (timezone.now() - order.notified_at) > timedelta(seconds=cooldown):
#                 vendor_serializer = VendorLogoSerializer(vendor, context={'request': request})
#                 payload = {
#                     "title": "Order Update by Manager",
#                     "body": f"Your order {token_no} is now ready.",
#                     "token_no": token_no,
#                     "status": status_to_update,
#                     "counter_no": order.counter_no,
#                     "name": vendor.name,
#                     "vendor_id": vendor.vendor_id,
#                     "location_id": vendor.location_id,
#                     "logo_url": vendor_serializer.data.get("logo_url", ""),
#                     "type": "foodstatus"
#                 }
#                 logger.info(f"📤 Web push payload prepared. Sending...")
#                 push_errors = notify_web_push(order, vendor, payload)
#                 logger.info(f"📤 Web push completed with {len(push_errors)} error(s).")
                

#                 order.notified_at = timezone.now()
#                 order.save(update_fields=['notified_at'])
#                 logger.info(f"🕒 Order {token_no} marked as notified at {order.notified_at}.")
#             else:
#                 logger.info(f"⏳ Skipping web push. Cooldown active for token {token_no}.")

#         response_msg = {
#             "success": True,
#             "message": "Order updated and notifications sent.",
#             "token_no": token_no,
#             "push_errors": push_errors if push_errors else [],
#         }

#         if push_errors:
#             logger.warning(f"⚠️ Partial push failures for order {token_no}: {push_errors}")
#             response_msg.update({
#                 "success": False,
#                 "message": "Order updated. FCM sent. Some web pushes failed.",
#                 "push_errors": push_errors
#             })
#             return Response(response_msg, status=status.HTTP_207_MULTI_STATUS)

#         logger.info(f"✅ Order {token_no} successfully updated and notifications dispatched.")
#         return Response(response_msg, status=status.HTTP_200_OK)

#     except Exception as e:
#         logger.exception("🔥 Unhandled exception in manager_order_update:")
#         return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def manager_order_update(request):
    try:
        logger.info("📥 PATCH /update_order")
        logger.info(f"IP: {request.META.get('REMOTE_ADDR')}, UA: {request.META.get('HTTP_USER_AGENT')}")
        logger.debug(f"Request Data: {request.data}")

        data = request.data
        token_no = data.get('token_no')
        if not token_no:
            logger.warning("⛔ token_no is required.")
            return Response({"message": "token_no is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token_no = int(data.get('token_no'))
        except (TypeError, ValueError):
            logger.warning("❌ token_no must be a valid integer.")
            return Response({"message": "token_no must be a valid integer."}, status=status.HTTP_400_BAD_REQUEST)

        manager = getattr(request.user, 'profile_roles', None)
        if not manager or not manager.exists():
            logger.warning("⚠️ No manager profile found for the user.")
            return Response({"message": "User is not a manager."}, status=status.HTTP_403_FORBIDDEN)

        manager = manager.first()
        if not manager.vendor:
            logger.warning("⚠️ Manager does not have an associated vendor.")
            return Response({"message": "Manager does not have an associated vendor."}, status=status.HTTP_403_FORBIDDEN)

        vendor = manager.vendor
        token_no = data['token_no']
        status_to_update = "ready"
        device = None  # Manager is not a customer device

        logger.info(f"🔧 Manager: {manager.name}, Vendor: {vendor.name} ({vendor.vendor_id}), Token: {token_no}, Status: {status_to_update}")

        order = update_existing_order_by_manager(token_no, vendor, device, status_to_update, manager)
        if not order:
            logger.warning(f"❌ No order found with token_no: {token_no} for vendor {vendor.name}")
            return Response({"message": f"Order with token_no {token_no} not found."}, status=status.HTTP_404_NOT_FOUND)

        logger.info(f"✅ Order found and updated: {order.id} — new status: {status_to_update}")

        # 🔔 Notify Android TV (FCM)
        fcm_success, fcm_info = notify_android_tv(vendor, data)
        logger.info(f"📺 Android TV FCM sent | Success: {fcm_success} | Info: {fcm_info}")

        # 🔔 Notify Customer (Web Push) — if "ready" and cooldown passed
        push_errors = []
        if status_to_update.lower() == "ready":
            from django.conf import settings
            cooldown = getattr(settings, "PUSH_COOLDOWN_SECONDS", 5)

            if not order.notified_at or (timezone.now() - order.notified_at) > timedelta(seconds=cooldown):
                vendor_serializer = VendorLogoSerializer(vendor, context={'request': request})
                payload = {
                    "title": "Order Update by Manager",
                    "body": f"Your order {token_no} is now ready.",
                    "token_no": token_no,
                    "status": status_to_update,
                    "counter_no": order.counter_no,
                    "name": vendor.name,
                    "vendor_id": vendor.vendor_id,
                    "location_id": vendor.location_id,
                    "logo_url": vendor_serializer.data.get("logo_url", ""),
                    "type": "foodstatus"
                }
                logger.info(f"📤 Web push payload prepared. Sending...")
                push_errors = notify_web_push(order, vendor, payload)
                logger.info(f"📤 Web push completed with {len(push_errors)} error(s).")

                order.notified_at = timezone.now()
                order.save(update_fields=['notified_at'])
                logger.info(f"🕒 Order {token_no} marked as notified at {order.notified_at}.")
            else:
                logger.info(f"⏳ Skipping web push. Cooldown active for token {token_no}.")

        # 🧾 Final response message
        response_msg = {
            "success": True,
            "message": "Order updated successfully.",
            "token_no": token_no,
            "android_tv": fcm_success,
            "android_tv_info": fcm_info,
            "web_push": not push_errors,
            "web_push_info": push_errors,
        }

        logger.info(f"✅ Order {token_no} successfully updated and all notifications dispatched.")
        return Response(response_msg, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception("🔥 Unhandled exception in manager_order_update:")
        return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)