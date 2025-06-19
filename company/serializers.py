from rest_framework import serializers
from vendors.models import Vendor, AndroidDevice, Device ,AdvertisementImage
from django.db.models import Q
import json

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_id', 'name', 'location']  

from rest_framework import serializers
from vendors.models import Vendor

class VendorDetailSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    menu_files = serializers.SerializerMethodField()
    android_tvs = serializers.SerializerMethodField()
    keypad_devices = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = [
            'id',
            'vendor_id',
            'name',
            'alias_name',
            'place_id',
            'location_id',
            'logo_url',
            'menu_files',
            'android_tvs',
            'keypad_devices',
        ]

    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            return request.build_absolute_uri(obj.logo.url).replace('http://', 'https://')
        return ''

    def get_menu_files(self, obj):
        request = self.context.get('request')
        try:
            menu_list = json.loads(obj.menus or "[]")  # assumes it's a JSON list like ["/media/menus/menu1.pdf", ...]
            full_menu_urls = []
            if request:
                for path in menu_list:
                    if not path.startswith("http"):
                        url = request.build_absolute_uri(f"/media/{path}")
                        full_menu_urls.append(url.replace("http://", "https://"))
                    else:
                        full_menu_urls.append(path)

            
            return list(full_menu_urls)
        except Exception:
            return []

    def get_android_tvs(self, obj):
        return list(obj.android_devices.values('mac_address')) if hasattr(obj, 'android_devices') else []

    def get_keypad_devices(self, obj):
        return list(obj.devices.values('serial_no')) if hasattr(obj, 'devices') else []

class UnmappedVendorDetailSerializer(serializers.ModelSerializer):
    unmapped_android_tvs = serializers.SerializerMethodField()
    unmapped_locations = serializers.SerializerMethodField()
    unmapped_keypad_devices = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = [
            'unmapped_android_tvs',
            'unmapped_locations',
            'unmapped_keypad_devices',
        ]

    def get_unmapped_android_tvs(self, obj):
        admin_outlet = obj.admin_outlet

        # Get unmapped and vendor-mapped android devices
        tvs = AndroidDevice.objects.filter(
            admin_outlet=admin_outlet
        ).filter(Q(vendor__isnull=True) | Q(vendor=obj)).values('mac_address')

        return list(tvs)
    
    def get_unmapped_locations(self, obj):
        admin_outlet = obj.admin_outlet
        current_location_code = obj.location_id

        try:
            all_locations = json.loads(admin_outlet.locations)
        except json.JSONDecodeError:
            return {'unmapped': []}

        used_codes = Vendor.objects.filter(
            admin_outlet=admin_outlet
        ).exclude(location_id=current_location_code).values_list('location_id', flat=True)

        unmapped = []

        for loc in all_locations:
            for name, code in loc.items():
                entry = {'key': name, 'value': code}
                if code not in used_codes:
                    unmapped.append(entry)

        return list(unmapped)
    
    def get_unmapped_keypad_devices(self, obj):
        admin_outlet = obj.admin_outlet
        unmapped = Device.objects.filter(
            admin_outlet=admin_outlet
        ).filter(Q(vendor__isnull=True) | Q(vendor=obj)).values('serial_no')
        return list(unmapped)

class VendorUpdateSerializer(serializers.Serializer):
    vendor_id = serializers.CharField(required=True)
    name = serializers.CharField(required=False, allow_blank=True)
    alias_name = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    place_id = serializers.CharField(required=False, allow_blank=True)
    location_id = serializers.CharField(required=False, allow_blank=True)

    def validate_vendor_id(self, value):
        if not Vendor.objects.filter(vendor_id=value).exists():
            raise serializers.ValidationError("Invalid vendor ID.")
        return value

    def validate_alias_name(self, value):
        vendor_id = self.initial_data.get('vendor_id')
        vendor = Vendor.objects.filter(vendor_id=vendor_id).first()
        if vendor and Vendor.objects.exclude(id=vendor.id).filter(alias_name__iexact=value).exists():
            raise serializers.ValidationError("Alias name already exists.")
        return value

    def validate_name(self, value):
        vendor_id = self.initial_data.get('vendor_id')
        vendor = Vendor.objects.filter(vendor_id=vendor_id).first()
        if vendor and Vendor.objects.exclude(id=vendor.id).filter(name__iexact=value).exists():
            raise serializers.ValidationError("Vendor name already exists.")
        return value

class AdvertisementImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AdvertisementImage
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url
