from django.contrib import admin
from .models import Vendor, Order, Device, PushSubscription

@admin.register(Vendor)
class VendorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location','vendor_id','created_at','updated_at')  # Display fields in the admin panel
    search_fields = ('name', 'location')       # Enable search functionality

@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('token_no', 'vendor', 'counter_no', 'status','updated_by','created_at','updated_at')
    list_filter = ('status', 'vendor')  # Filter by status and restaurant
    search_fields = ('token_no',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('serial_no', 'vendor','created_at','updated_at')
    list_filter = ('serial_no', 'vendor')  # Filter by status and restaurant
    search_fields = ('serial_no',)


@admin.register(PushSubscription)
class PushSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'browser_id', 'endpoint', 'display_tokens')
    search_fields = ('browser_id', 'endpoint')
    list_filter = ('browser_id',)

    def display_tokens(self, obj):
        # Convert each token_no to str before joining
        return ", ".join(str(order.token_no) for order in obj.tokens.all())
    display_tokens.short_description = 'Tokens'
