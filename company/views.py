import json
import logging
import random

from django.db import transaction
from django.db.models import Q
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

from static.utils.functions.validation import validate_fields
from .serializers import (VendorSerializer,
                          VendorDetailSerializer,
                          UnmappedVendorDetailSerializer,
                          VendorUpdateSerializer
                          )
@login_required
def dashboard(request):
    return render(request, 'company/dashboard.html')

@login_required
def outlets(request):
    return render(request, 'company/outlets.html')

@login_required
def configurations(request):
    return render(request, "company/configurations.html")

@login_required(login_url='/login/')
def create_outlet(request):
    return render(request, 'company/create_outlet.html')

@login_required
def update_outlet_page(request):
    return render(request, "company/update_outlet.html")

@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def get_vendor_details(request):
    vendor_id = request.GET.get('vendor_id')
    
    if not vendor_id:
        return Response({'error': 'Vendor ID not provided'}, status=400)
    try:
        vendor = Vendor.objects.get(vendor_id=vendor_id)
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=400)
    
    serializer = VendorDetailSerializer(
        vendor, context={'request': request}
        ).data

    unmapped_vendors_data = UnmappedVendorDetailSerializer(
        vendor, context={'request': request}
        ).data
    
    return Response({
        "vendor_data": serializer,
        "unmapped_data":unmapped_vendors_data,
        "message": "Success"
        }, status=200)

@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def get_vendors(request):
    user = request.user
    try:
        admin_outlet = user.admin_outlet
    except AdminOutlet.DoesNotExist:
        return Response(
            {"error": "AdminOutlet not found for this user."}
            , status=404)

    vendors = admin_outlet.vendors.all()
    vendors_data = VendorSerializer(vendors, many=True).data
       
    return Response(
        {"vendors": vendors_data, "message": "Success"}
        , status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outlet_creation_data(request):
    user = request.user
    try:
        admin_outlet = user.admin_outlet
    except AdminOutlet.DoesNotExist:
        return Response(
            {'error': 'Invalid customer_id'}
            ,status=status.HTTP_404_NOT_FOUND)

    # Parse all locations from JSON field
    try:
        locations_data = json.loads(admin_outlet.locations)
    except json.JSONDecodeError:
        return Response(
            {'error': 'Invalid locations JSON'}
            , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Get all location codes already used in vendors
    mapped_codes = Vendor.objects.filter(
        admin_outlet=admin_outlet
        ).values_list('location_id', flat=True)

    # Filter unmapped locations
    unmapped_locations = []
    for location in locations_data:
        for name, code in location.items():
            if code not in mapped_codes:
                unmapped_locations.append({'key': name, 'value': code})

    # Get unmapped keypad devices
    available_keypads = Device.objects.filter(
        admin_outlet=admin_outlet, vendor__isnull=True
        ).values('serial_no')

    # Get unmapped Android TVs
    available_android_tvs = AndroidDevice.objects.filter(
        admin_outlet=admin_outlet, vendor__isnull=True
        ).values('mac_address')

    return Response({
        'locations': unmapped_locations,
        'keypad_devices': list(available_keypads),
        'android_tvs': list(available_android_tvs),
    }, status=status.HTTP_200_OK)

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
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
@transaction.atomic
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

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
@transaction.atomic
def update_vendor(request):
    try:
        serializer = VendorUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=400)

        validated_data = serializer.validated_data
        vendor = Vendor.objects.get(vendor_id=validated_data['vendor_id'])
        # Update basic fields if provided
        for field in ['name', 'alias_name', 'location', 'place_id', 'location_id']:
            value = validated_data.get(field)
        if value:
            setattr(vendor, field, value.strip())

        # Update logo
        logo_file = request.FILES.get('logo')
        if logo_file:
                # Delete existing file if it exists.
            if vendor.logo and default_storage.exists(vendor.logo.name):
                default_storage.delete(vendor.logo.name)

            logo_path = default_storage.save('vendor_logos/' + logo_file.name, ContentFile(logo_file.read()))
            vendor.logo = logo_path

        # Update menus
        menu_files = request.FILES.getlist('menus')
        if menu_files:
            if vendor.menus:
                try:
                    old_menu_paths = json.loads(vendor.menus)
                    for old_path in old_menu_paths:
                        if old_path and default_storage.exists(old_path):
                            default_storage.delete(old_path)
                except json.JSONDecodeError:
                    pass  # In case menus field isn't valid JSON.
                
            menu_paths = []
            for file in menu_files:
                path = default_storage.save('menus/' + file.name, ContentFile(file.read()))
                menu_paths.append(path)
            vendor.menus = json.dumps(menu_paths)

        vendor.save()

        # Update device mappings
        device_serials = request.data.getlist('device_mapping[]')
        if device_serials:
            # Unmap all devices previously linked to this vendor
            vendor.devices.update(vendor=None)
            for serial in device_serials:
                try:
                    device = Device.objects.get(serial_no=serial)
                    device.vendor = vendor
                    device.save()
                except Device.DoesNotExist:
                    pass

        #Update TV (AndroidDevice) mappings
        mac_addresses = request.data.getlist('tv_mapping[]')
        if mac_addresses:
            vendor.android_devices.update(vendor=None)
            for mac in mac_addresses:
                try:
                    android_device = AndroidDevice.objects.get(mac_address=mac)
                    android_device.vendor = vendor
                    android_device.save()
                except AndroidDevice.DoesNotExist:
                    pass

        return Response({
            'message': 'Vendor updated successfully.',
            'vendor_id': vendor.vendor_id,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


