from rest_framework import serializers
from vendors.models import Order,UserProfile

class OrdersSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    manager_id = serializers.PrimaryKeyRelatedField(
        source='user_profile',
        queryset=UserProfile.objects.all(),
        required=False,
    )
    manager_name = serializers.CharField(source='user_profile.name', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        extra_fields = ['vendor_name', 'manager_id', 'manager_name']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        # Rename vendor name again if needed
        rep['name'] = instance.vendor.name

        # Remove the original user_profile key from output
        rep.pop('user_profile', None)

        return rep

