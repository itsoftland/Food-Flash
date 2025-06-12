from rest_framework import serializers
from vendors.models import Vendor

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
            'location',
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
            menu_files = obj.menufile_set.all()
            return [request.build_absolute_uri(f.file.url).replace("http://", "https://") for f in menu_files]
        except:
            return []

    def get_android_tvs(self, obj):
        return list(obj.android_devices.values('mac_address')) if hasattr(obj, 'android_devices') else []

    def get_keypad_devices(self, obj):
        return list(obj.devices.values('serial_no')) if hasattr(obj, 'devices') else []
