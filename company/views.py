import json
import logging
import random

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from vendors.models import Vendor, Device, AdminOutlet, AndroidDevice

from static.utils.validation import validate_fields

@login_required
def dashboard(request):
    return render(request, 'company/dashboard.html')

@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def get_vendors(request):
    user = request.user

    try:
        admin_outlet = user.admin_outlet
    except AdminOutlet.DoesNotExist:
        return Response({"detail": "AdminOutlet not found for this user."}, status=404)

    vendors = admin_outlet.vendors.all()

    return Response({"vendor_ids": [v.id for v in vendors], "message": "Success"}, status=200)



# @login_required
# def dashboard(request):
#     try:
#         admin_outlet = request.user.admin_outlet 
#         vendors = request.user.admin_outlet.vendors.all()
#     except:
#         return redirect('/login')
#     context = {
#         'admin_outlet': admin_outlet,
#         'added_vendors': vendors,
#     }
#     return render(request, 'company/dashboard.html', context)

@login_required(login_url='/login/')
def create_outlet(request):
    admin_outlet = request.user.admin_outlet
    
    # Parse the locations JSON
    locations_data = json.loads(admin_outlet.locations)
    
    # Get all location codes already mapped to a vendor under this outlet
    mapped_codes = Vendor.objects.filter(admin_outlet=admin_outlet).values_list('location_id', flat=True)

    # Filter only unmapped locations
    unmapped_locations = []
    for location in locations_data:
        for name, code in location.items():
            if code not in mapped_codes:
                unmapped_locations.append({'key': name, 'value': code})
    # Get available unmapped devices
    devices = Device.objects.filter(admin_outlet=admin_outlet, vendor__isnull=True)
    available_android_tvs = AndroidDevice.objects.filter(admin_outlet=admin_outlet, vendor__isnull=True)

    return render(request, 'company/create_outlet.html', {
        'locations': unmapped_locations,
        'devices': devices,
        'android_devices': available_android_tvs,
        'admin_outlet': admin_outlet
    })


def generate_unique_vendor_id():
    while True:
        # Generate a random 6-digit number, first digit 1-9
        vendor_id = random.randint(100000, 999999)
        if not Vendor.objects.filter(vendor_id=vendor_id).exists():
            return vendor_id
        
@api_view(['POST'])
@validate_fields(['customer_id', 'name', 'location', 'place_id',
                  'location_id','logo','menu_files','device_mapping[]',
                  'tv_mapping[]', 'alias_name'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def create_vendor(request):
    try:
        print(request.data)
        customer_id = request.data.get('customer_id')
        admin_outlet = get_object_or_404(AdminOutlet, customer_id=customer_id)

        name = request.data.get('name')
        alias_name = request.data.get('alias_name')
        location = request.data.get('location')
        place_id = request.data.get('place_id', '')
        location_id = request.data.get('location_id')
        if Vendor.objects.filter(name__iexact=name).exists():
            return Response({
                'success': False,
                'error': 'Vendor with this name already exists.'
            }, status=status.HTTP_409_CONFLICT)

        # Generate unique vendor_id
        vendor_id = generate_unique_vendor_id()

        # Handle logo file upload
        logo_file = request.FILES.get('logo')
        logo_path = None
        if logo_file:
            logo_path = default_storage.save('vendor_logos/' + logo_file.name, ContentFile(logo_file.read()))

        # Handle multiple menu files
        menu_files = request.FILES.getlist('menu_files')
        menu_paths = []
        for file in menu_files:
            path = default_storage.save('menus/' + file.name, ContentFile(file.read()))
            menu_paths.append(path)

        # Create Vendor instance
        vendor = Vendor.objects.create(
            admin_outlet=admin_outlet,
            name=name,
            alias_name=alias_name,
            location=location,
            place_id=place_id,
            vendor_id=vendor_id,
            location_id=location_id,
            logo=logo_path,
            menus=json.dumps(menu_paths),
        )
        # Handle multiple Device mappings (serial numbers)
        device_serials = request.data.getlist('device_mapping[]')
        for serial in device_serials:
            try:
                device = Device.objects.get(serial_no=serial)
                device.vendor = vendor
                device.save()
            except Device.DoesNotExist:
                pass  # Optional: log or collect errors

        # Handle multiple AndroidDevice mappings (MAC addresses)
        mac_addresses = request.data.getlist('tv_mapping[]')
        for mac in mac_addresses:
            try:
                android_device = AndroidDevice.objects.get(mac_address=mac)
                android_device.vendor = vendor
                android_device.save()
            except AndroidDevice.DoesNotExist:
                pass  # Optional: log or collect errors

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

# views.py
def update_outlet_page(request):
    return render(request, "company/update_outlet.html")

