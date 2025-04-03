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
        order = Order.objects.get(token_no=token_no)
        data = {
            'vendor': order.vendor.name,
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
            vendor = Vendor.objects.get(vendor_id=vendor_id)
            new_order_data = {
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
            "logo": f"{settings.MEDIA_URL}{outlet.logo}" if outlet.logo else None
        }
        for outlet in outlets
    ]

    return Response(data, status=status.HTTP_200_OK)
