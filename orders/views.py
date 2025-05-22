from rest_framework.decorators import api_view,permission_classes 
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from vendors.serializers import OrdersSerializer
from .serializers import VendorLogoSerializer
from vendors.models import Order,Vendor,AdminOutlet,Device
from django.core.cache import cache

def outlet_selection(request):
    location_id = request.GET.get("location_id")
    context = {}  # Add any extra context here if needed

    response = render(request, "orders/landing_page.html", context)

    if location_id:
        # Set cookie for 30 days (optional: domain='yourdomain.com' if needed)
        response.set_cookie("location_id", location_id, max_age=30 * 24 * 60 * 60)

    return response

def home(request):
    cache.clear()
    return render(request, 'orders/index.html')

def company_registration(request):
    cache.clear()
    return render(request, 'orders/superadmin/company_registration.html')

def token_display(request):
    cache.clear()
    return render(request, 'orders/token_display.html')

from .serializers import AdminOutletSerializer
import json

def preprocess_request_data(data):
    return {
        'user': {
            'username': data.get('CustomerUsername'),
            'password': data.get('CustomerPassword'),
        },
        'customer_name': data.get('CustomerName'),
        'phone_number': data.get('PhoneNumber'),
        'customer_email': data.get('CustomerEmail'),
        'gst_number': data.get('GSTNumber'),
        'customer_contact_person': data.get('CustomerContactPerson'),
        'customer_contact': data.get('CustomerContact'),
        'customer_address': data.get('CustomerAddress'),
        'customer_address2': data.get('CustomerAddress2'),
        'customer_state': data.get('CustomerState'),
        'customer_city': data.get('CustomerCity'),
        # New fields
        'authentication_status': data.get('Authenticationstatus'),
        'product_registration_id': data.get('ProductRegistrationId'),
        'unique_identifier': data.get('UniqueIDentifier'),
        'customer_id': data.get('CustomerId'),
        'product_from_date': data.get('ProductFromDate'),
        'product_to_date': data.get('ProductToDate'),
        'total_count': data.get('TotalCount'),
        'project_code': data.get('ProjectCode'),
        'web_login_count': data.get('WebLoginCount'),
        'android_tv_count': data.get('AndroidTvCount'),
        'android_apk_count': data.get('AndroidApkCount'),
        'keypad_device_count': data.get('KeypadDeviceCount'),
        'led_display_count': data.get('LedDisplayCount'),
        'outlet_count': data.get('OutletCount'),
        'locations': json.loads(data.get('Locations', '[]')),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register_company(request):
    data = preprocess_request_data(request.data)

    # Duplicate check for company name and email
    if AdminOutlet.objects.filter(
        customer_name=data.get('customer_name'),
        customer_email=data.get('customer_email')
    ).exists():
        return Response(
            {"error": "A company with the same name and email already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Duplicate check for username in User model
    username = data.get('user', {}).get('username')
    if username and AdminOutlet.objects.filter(user__username=username).exists():
        return Response(
            {"error": "Username already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = AdminOutletSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Company registered successfully"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def check_status(request):
    token_no = request.GET.get('token_no')
    vendor_id = request.GET.get('vendor_id')

    # Validate presence
    if not token_no:
        return Response({'error': 'Token number is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if not vendor_id:
        return Response({'error': 'Vendor ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate integer format
    try:
        token_no = int(token_no)
        if token_no <= 0:
            return Response({'error': 'Token number must be a positive integer.'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Token number must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        vendor_id = int(vendor_id)
    except ValueError:
        return Response({'error': 'Vendor ID must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Try to fetch the existing order by token_no
        order = Order.objects.get(token_no=token_no, vendor__vendor_id=vendor_id)
        vendor_serializer = VendorLogoSerializer(order.vendor, context={'request': request})
        logo_url = vendor_serializer.data.get('logo_url', '')
        data = {
            'name': order.vendor.name,
            'vendor': order.vendor.id,
            'token_no': order.token_no,
            'status': order.status,
            'counter_no': order.counter_no,
            'message': 'Order retrieved successfully.',
            "vendor_id": order.vendor.vendor_id,
            "location_id": order.vendor.location_id,
            "logo_url": logo_url,
            "type": "foodstatus"
        }
        
        return Response(data, status=status.HTTP_200_OK)

    except Order.DoesNotExist:
        try:
            # Create new order with status 'preparing'
            vendor = Vendor.objects.get(vendor_id=vendor_id)
            new_order_data = {
                'name': vendor.name,
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
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)
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

from .serializers import VendorLogoSerializer,VendorMenuSerializer  

@api_view(['POST'])
@permission_classes([AllowAny])
def get_vendor_logos(request):
    try:
        vendor_ids = request.data.get("vendor_ids")
        
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
        
from .serializers import VendorAdsSerializer,FeedbackSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def get_vendor_ads(request):
    try:
        vendor_ids = request.data.get("vendor_ids")

        if not vendor_ids or not isinstance(vendor_ids, list):
            return Response({"error": "vendor_ids must be provided as a list."}, status=400)

        vendors = Vendor.objects.filter(vendor_id__in=vendor_ids)

        # ✅ Use serializer to convert ad paths to full URLs
        serializer = VendorAdsSerializer(vendors, many=True, context={'request': request})
        return Response(serializer.data, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def get_vendor_menus(request):
    try:
        vendor_ids = request.data.get("vendor_ids")

        if not vendor_ids or not isinstance(vendor_ids, list):
            return Response({"error": "vendor_ids must be provided as a list."}, status=400)

        vendors = Vendor.objects.filter(vendor_id__in=vendor_ids)

        serializer = VendorMenuSerializer(vendors, many=True, context={'request': request})
        return Response(serializer.data, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_feedback(request):
    vendor_id = request.data.get('vendor_id')

    if not vendor_id:
        return Response({'success': False, 'message': 'Vendor ID is required'}, status=400)

    try:
        vendor = Vendor.objects.get(vendor_id=vendor_id)
    except Vendor.DoesNotExist:
        return Response({'success': False, 'message': 'Vendor not found'}, status=404)

    # Prepare the complete data dictionary
    data = {
        'vendor': vendor.id,  # actual primary key
        'feedback_type': request.data.get('feedback_type'),
        'category': request.data.get('category'),
        'name': request.data.get('name'),
        'comment': request.data.get('comment'),
    }

    serializer = FeedbackSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Feedback submitted successfully'}, status=201)
    else:
        return Response({'success': False, 'errors': serializer.errors}, status=400)


from vendors.serializers import OrdersSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_recent_ready_orders(request):
    try:
        vendor_id = request.GET.get('vendor_id')
        if not vendor_id:
            return Response({"error": "vendor_id required"}, status=400)

        # Filter recent 'ready' orders for the given vendor
        recent_orders = Order.objects.filter(
            vendor__vendor_id=vendor_id,
            status='ready'
        ).order_by('-updated_at')[:8]

        # Serialize and add 'is_new' field
        data = []
        for order in recent_orders:
            serialized = OrdersSerializer(order, context={'request': request}).data
            serialized['is_new'] = not order.shown_on_tv
            data.append(serialized)

        # Mark these orders as shown
        Order.objects.filter(id__in=[order.id for order in recent_orders], shown_on_tv=False).update(shown_on_tv=True)

        return Response(data, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


from django.contrib.auth import authenticate, login , logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from vendors.models import AdminOutlet

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from vendors.models import AdminOutlet, Vendor  # adjust if models are elsewhere

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Check user type
            if user.is_superuser:
                return redirect('/superadmin_dashboard/')
            elif AdminOutlet.objects.filter(user=user).exists():
                return redirect('/company_dashboard/')
            elif Vendor.objects.filter(user=user).exists():
                return redirect('/outlet_dashboard/')
            else:
                return render(request, 'orders/login.html', {'error': 'User type not recognized'})
        else:
            return render(request, 'orders/login.html', {'error': 'Invalid username or password'})

    return render(request, 'orders/login.html')


@login_required
def company_dashboard(request):
    try:
        admin_outlet = request.user.admin_outlet 
    except AdminOutlet.DoesNotExist:
        return redirect('/login')

    context = {
        'admin_outlet': admin_outlet
    }
    return render(request, 'orders/company/company_dashboard.html', context)

@login_required
def superadmin_dashboard(request):
    # Superadmin check - not linked to AdminOutlet or Vendor
    is_admin_outlet = AdminOutlet.objects.filter(user=request.user).exists()
    # is_vendor = Vendor.objects.filter(user=request.user).exists()

    if is_admin_outlet:
        return redirect('/login')

    # Optionally pass users, companies, outlets etc. to the dashboard
    context = {
        'user': request.user,
        'admin_outlets': AdminOutlet.objects.all(),
        'vendors': Vendor.objects.all(),
    }
    return render(request, 'orders/superadmin/superadmin_dashboard.html', context)

@login_required
def outlet_dashboard(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        return redirect('/login')

    context = {
        'vendor': vendor,
    }
    return render(request, 'orders/outlet/outlet_dashboard.html', context)


def logout_view(request):
    logout(request)
    return redirect('loginview')  # or wherever you want to redirect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from vendors.models import AdminOutlet

@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # Or AllowAny if you want
def update_admin_outlet(request):
    customer_id = request.data.get('customer_id')
    if not customer_id:
        return Response({"error": "customer_id is required."},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        admin_outlet = AdminOutlet.objects.get(customer_id=customer_id)
    except AdminOutlet.DoesNotExist:
        return Response({"error": "AdminOutlet not found for this customer_id."},
                        status=status.HTTP_404_NOT_FOUND)

    # Ensure username is NOT changed, so remove user data or ignore it
    data = request.data.copy()
    if 'user' in data:
        data.pop('user')

    serializer = AdminOutletSerializer(admin_outlet, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render, redirect
import json

def create_outlet(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        place_id = request.POST.get('place_id')
        device_mapping_id = request.POST.get('device_mapping')
        logo = request.FILES.get('logo')

        Vendor.objects.create(
            name=name,
            location=location,
            place_id=place_id,
            logo=logo,
            device_mapping_id=device_mapping_id if device_mapping_id else None
        )
        return redirect('company_dashboard')

    # Assuming this JSON comes from DB or settings
    admin_outlet = request.user.admin_outlet
    locations_json = admin_outlet.locations
    locations_data = json.loads(locations_json)
    locations = [{'key': list(i.keys())[0], 'value': list(i.values())[0]} for i in locations_data]

    devices = Device.objects.all()
    return render(request, 'orders/company/create_outlet.html', {
        'locations': locations,
        'devices': devices,
        'admin_outlet':admin_outlet
    })
