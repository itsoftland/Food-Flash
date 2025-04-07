from rest_framework import serializers
from vendors.models import Vendor

class VendorLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'logo','vendor_id']  # 'logo' should be an ImageField

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and hasattr(instance.logo, 'url'):
            data['logo_url'] = request.build_absolute_uri(instance.logo.url)
        else:
            data['logo_url'] = ''
        data.pop('logo')  # Optional: remove raw logo field
        return data

class VendorAdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_id', 'ads', 'name']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        # Process JSON string of ads and convert to full URLs
        ad_paths = instance.get_ads_list()
        full_ad_urls = []

        if request:
            for path in ad_paths:
                if not path.startswith("http"):
                    full_ad_urls.append(request.build_absolute_uri(f"/media/{path}"))
                else:
                    full_ad_urls.append(path)
        
        data['ads'] = full_ad_urls
        return data
