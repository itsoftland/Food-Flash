from rest_framework import serializers
from .models import Order

class OrdersSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'  # This will include vendor (as ID), token_no, status, etc.
        # Add vendor_name manually even though it's not in the model
        extra_fields = ['name']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['name'] = instance.vendor.name  # Just to be extra safe
        return rep
