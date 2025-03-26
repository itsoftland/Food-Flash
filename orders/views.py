from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from vendors.serializers import OrdersSerializer
from vendors.models import Order,Vendor
from django.core.cache import cache

def home(request):
    cache.clear()
    return render(request, 'orders/index.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def check_status(request):
    token_no = request.GET.get('token_no')
    
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
            vendor = Vendor.objects.get(id=1)
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


