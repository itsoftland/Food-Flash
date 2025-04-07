from django.contrib import admin
from .models import Vendor, Order, Device, PushSubscription, AdminOutlet

@admin.register(AdminOutlet)
class AdminOutletAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'phone', 'created_at')
    
# @admin.register(Vendor)
# class VendorsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'location_id','location','admin_outlet','vendor_id','created_at','updated_at')  # Display fields in the admin panel
#     list_filter = ('admin_outlet', 'location_id','name')      # Enable search functionality

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

from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json

from .models import Vendor
from .forms import VendorFileUploadForm

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'vendor_id')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-files/', self.admin_site.admin_view(self.upload_files_view), name='vendor-upload-files'),
        ]
        return custom_urls + urls

    def upload_files_view(self, request):
        form = VendorFileUploadForm(request.POST or None, request.FILES or None)

        if request.method == 'POST':
            print("POST DATA:", request.POST)
            print("FILES:", request.FILES)
            if not form.is_valid():
                print("FORM ERRORS:", form.errors)
                print("IS FORM VALID:", form.is_valid())

            vendor = form.cleaned_data['vendor']
            ads_files = request.FILES.getlist('ads_files')
            menus_files = request.FILES.getlist('menus_files')

            ads_paths = json.loads(vendor.ads or "[]")
            menus_paths = json.loads(vendor.menus or "[]")

            for file in ads_files:
                path = default_storage.save('ads/' + file.name, ContentFile(file.read()))
                ads_paths.append(path)

            for file in menus_files:
                path = default_storage.save('menus/' + file.name, ContentFile(file.read()))
                menus_paths.append(path)

            vendor.ads = json.dumps(ads_paths)
            vendor.menus = json.dumps(menus_paths)
            vendor.save()
            

            self.message_user(request, "Files uploaded successfully.")
            return redirect("..")

        # 🛠 Fix: Add admin context to avoid KeyError
        context = {
            **self.admin_site.each_context(request),  # ✅ This adds 'available_apps' and other admin vars
            'form': form,
            'title': "Upload Vendor Files (Testing)",
        }

        return render(request, 'admin/vendor_upload_files.html', context)

