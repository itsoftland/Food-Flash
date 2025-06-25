from rest_framework import serializers
from vendors.models import (Vendor,AndroidDevice,
                            Device ,AdvertisementImage,
                            AdvertisementProfile,
                            AdvertisementProfileAssignment)
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

class AdvertisementProfileSerializer(serializers.ModelSerializer):
    image_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    
    images = AdvertisementImageSerializer(many=True, read_only=True)

    class Meta:
        model = AdvertisementProfile
        fields = [
            'id',
            'name',
            'date_start',
            'date_end',
            'days_active',
            'priority',
            'image_ids',
            'images',
            'created_at',
        ]

    def get_images(self, obj):
        return [img.id for img in obj.images.all()]

    def validate_image_ids(self, value):
        request = self.context.get('request')
        if not request or not hasattr(request.user, 'admin_outlet'):
            raise serializers.ValidationError("User context or admin outlet missing.")

        images = AdvertisementImage.objects.filter(
            id__in=value,
            admin_outlet=request.user.admin_outlet
        )

        if images.count() != len(set(value)):
            raise serializers.ValidationError("Some image IDs are invalid or not allowed.")

        return list(images)

    def create(self, validated_data):
        images = validated_data.pop('image_ids', [])
        profile = AdvertisementProfile.objects.create(
            admin_outlet=self.context['request'].user.admin_outlet,
            **validated_data
        )
        profile.images.set(images)
        return profile
    
    def validate(self, attrs):
        date_start = attrs.get('date_start')
        date_end = attrs.get('date_end')
        days_active = attrs.get('days_active')

        has_dates = date_start and date_end
        has_days = bool(days_active)

        if not (has_dates or has_days):
            raise serializers.ValidationError(
                "Either both start & end dates OR at least one active day must be provided."
            )

        return attrs

class AdvertisementProfileAssignmentSerializer(serializers.Serializer):
    vendor_ids = serializers.ListField(
        child=serializers.IntegerField(), required=True
    )
    profile_ids = serializers.ListField(
        child=serializers.IntegerField(), required=True
    )

    def validate(self, data):
        vendor_ids = data.get('vendor_ids')
        profile_ids = data.get('profile_ids')

        if not vendor_ids:
            raise serializers.ValidationError("vendor_ids is required and cannot be empty.")
        if not profile_ids:
            raise serializers.ValidationError("profile_ids is required and cannot be empty.")

        return data
    def create(self, validated_data):
        vendor_ids = validated_data['vendor_ids']
        profile_ids = validated_data['profile_ids']

        vendors = Vendor.objects.filter(vendor_id__in=vendor_ids)
        profiles = AdvertisementProfile.objects.filter(id__in=profile_ids)

        assigned_count = 0
        skipped_count = 0

        for vendor in vendors:
            for profile in profiles:
                if AdvertisementProfileAssignment.objects.filter(profile=profile, vendor=vendor).exists():
                    skipped_count += 1
                else:
                    AdvertisementProfileAssignment.objects.create(profile=profile, vendor=vendor)
                    assigned_count += 1

        return {
            'vendor_count': vendors.count(),
            'profile_count': profiles.count(),
            'total_assigned': assigned_count,
            'skipped': skipped_count
        }

    # def create(self, validated_data):
    #     vendor_ids = validated_data['vendor_ids']
    #     profile_ids = validated_data['profile_ids']

    #     vendors = Vendor.objects.filter(id__in=vendor_ids)
    #     profiles = AdvertisementProfile.objects.filter(id__in=profile_ids)

    #     created = []
    #     skipped = []

    #     for vendor in vendors:
    #         for profile in profiles:
    #             if AdvertisementProfileAssignment.objects.filter(profile=profile, vendor=vendor).exists():
    #                 skipped.append({
    #                     'vendor_id': vendor.id,
    #                     'vendor_name': vendor.name,
    #                     'profile_id': profile.id,
    #                     'profile_name': profile.name
    #                 })
    #                 continue

    #             assignment = AdvertisementProfileAssignment.objects.create(profile=profile, vendor=vendor)
    #             created.append({
    #                 'vendor_id': vendor.id,
    #                 'vendor_name': vendor.name,
    #                 'profile_id': profile.id,
    #                 'profile_name': profile.name,
    #                 'assigned_at': assignment.assigned_at
    #             })

    #     return {
    #         'assigned': created,
    #         'skipped': skipped
    #     }


class AdvertisementProfileMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementProfile
        fields = ['id', 'name']
