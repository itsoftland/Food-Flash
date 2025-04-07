from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from vendors.serializers import OrdersSerializer
from vendors.models import Order,Vendor
from django.core.cache import cache

def outlet_selection(request):
    return render(request, "orders/outlet_selection.html")

def home(request):
    cache.clear()
    return render(request, 'orders/index.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def check_status(request):
    token_no = request.GET.get('token_no')
    vendor_id = request.GET.get('vendor_id')
    print(vendor_id)
    
    if not token_no:
        return Response({'error': 'Token number is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Try to fetch the existing order by token_no
        order = Order.objects.get(token_no=token_no,vendor__vendor_id=int(vendor_id))
        print("new vendor name",order.vendor.name)
        data = {
            'vendor_name': order.vendor.name,
            'token_no': order.token_no,
            'status': order.status,
            'counter_no':order.counter_no,
            'message': 'Order retrieved successfully.'
        }
        return Response(data, status=status.HTTP_200_OK)
    
    except Order.DoesNotExist:
        try:
            # If order not found, create a new one with status 'preparing'
            # Here, we assume a default vendor (e.g., vendor with id=1)
            vendor = Vendor.objects.get(vendor_id=int(vendor_id))
            print("vendor name",vendor.name)
            new_order_data = {
                'vendor_name':vendor.name,
                'token_no': token_no,
                'vendor': vendor.id,
                'status': 'preparing',
            }
            serializer = OrdersSerializer(data=new_order_data)
            if serializer.is_valid():
                serializer.save()
                data = serializer.data
                data['message'] = 'Order created with status preparing.'
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
from django.conf import settings
@api_view(['GET'])
@permission_classes([AllowAny])
def get_outlets(request):
    location_id = request.GET.get('location_id', None)  # Fetch location ID from query params
    
    if not location_id:
        return Response({"error": "Location ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    outlets = Vendor.objects.filter(location_id=location_id)
    
    data = [
        {
            "id": outlet.id,
            "name": outlet.name,
            "logo": f"{settings.MEDIA_URL}{outlet.logo}" if outlet.logo else None,
            "vendor_id":outlet.vendor_id
        }
        for outlet in outlets
    ]

    return Response(data, status=status.HTTP_200_OK)

from .serializers import VendorLogoSerializer  # We’ll define this below

@api_view(['POST'])
@permission_classes([AllowAny])
def get_vendor_logos(request):
    try:
        vendor_ids = request.data.get("vendor_ids")
        print(f"Received vendor_ids: {vendor_ids} | Type: {type(vendor_ids)}")
        
        # Validate input
        if vendor_ids is None or not isinstance(vendor_ids, list):
            return Response(
                {"error": "vendor_ids must be provided as a list."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure each ID is an integer
        if not all(isinstance(v_id, int) for v_id in vendor_ids):
            return Response(
                {"error": "All vendor_ids must be integers."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filter using vendor_id, not id
        vendors = Vendor.objects.filter(vendor_id__in=vendor_ids)

        if not vendors.exists():
            return Response(
                {"error": "No matching vendors found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serialized = VendorLogoSerializer(vendors, many=True, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {"error": "An unexpected error occurred.", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )