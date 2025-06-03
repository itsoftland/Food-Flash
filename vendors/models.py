from django.db import models
import json
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class AdminOutlet(models.Model):  
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='admin_outlet',
        null=True, blank=True
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    gst_number = models.CharField(max_length=100, blank=True, null=True)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_contact_person = models.CharField(max_length=255, blank=True, null=True)
    customer_address = models.TextField(blank=True, null=True)
    customer_address2 = models.TextField(blank=True, null=True)
    customer_city = models.CharField(max_length=100, blank=True, null=True)
    customer_state = models.CharField(max_length=100, blank=True, null=True)
    customer_contact = models.CharField(max_length=20, blank=True, null=True)
    authentication_status = models.CharField(max_length=50, default='Pending')
    product_registration_id = models.IntegerField(blank=True, null=True)
    unique_identifier = models.CharField(max_length=100, blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    product_from_date = models.DateTimeField(blank=True, null=True)
    product_to_date = models.DateTimeField(blank=True, null=True)
    total_count = models.CharField(max_length=10, blank=True, null=True)
    project_code = models.CharField(max_length=100, blank=True, null=True)
    web_login_count = models.IntegerField(blank=True, null=True)
    android_tv_count = models.IntegerField(blank=True, null=True)
    android_apk_count = models.IntegerField(blank=True, null=True)
    keypad_device_count = models.IntegerField(blank=True, null=True)
    led_display_count = models.IntegerField(blank=True, null=True)
    outlet_count = models.IntegerField(blank=True, null=True)
    locations = models.JSONField(blank=True, null=True) 
    
    customer_email = models.EmailField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_name

class Vendor(models.Model):
    user = models.OneToOneField(
    User, on_delete=models.CASCADE, related_name='vendor',
    null=True, blank=True
    )
    admin_outlet = models.ForeignKey(AdminOutlet, on_delete=models.CASCADE, related_name='vendors')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    place_id = models.CharField(max_length=255, blank=True, null=True)
    vendor_id = models.IntegerField(unique=True)
    location_id = models.CharField(max_length=20)  # Unique ID for each location
    logo = models.ImageField(upload_to='vendor_logos/', blank=True, null=True)
    ads = models.TextField(blank=True, null=True)    # Stores JSON string of paths
    menus = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_ads_list(self):
        return json.loads(self.ads or "[]")

    def get_menus_list(self):
        return json.loads(self.menus or "[]")
    
    def __str__(self):
        return f"{self.name} - {self.admin_outlet.customer_name}"

class Device(models.Model):
    serial_no = models.CharField(max_length=255, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="devices",null=True,blank=True)
    admin_outlet = models.ForeignKey(AdminOutlet, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.serial_no

class Order(models.Model):
    STATUS_CHOICES = [
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
    ]
    USER_CHOICES = [
        ('client', 'Client'),
        ('customer', 'Customer'),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="orders")
    device = models.ForeignKey(Device, on_delete=models.CASCADE,null=True, blank=True, related_name="orders")
    token_no = models.IntegerField(validators=[
            MinValueValidator(0),
            MaxValueValidator(9999)
        ])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preparing')
    counter_no = models.IntegerField(default=1)
    shown_on_tv = models.BooleanField(default=False)
    notified_at = models.DateTimeField(null=True, blank=True, default=None)
    updated_by = models.CharField(max_length=20, choices=USER_CHOICES, default='client')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('token_no', 'vendor') 

    def __str__(self):
        return f"Token {self.token_no}"

class PushSubscription(models.Model):
    browser_id = models.CharField(max_length=255, unique=True)
    endpoint = models.TextField(unique=True)
    p256dh = models.TextField()
    auth = models.TextField()
    tokens = models.ManyToManyField(Order, blank=True)  # Many-to-Many with orders

    def __str__(self):
        return f"Subscription for {self.browser_id}"

class Feedback(models.Model):
    TYPE_CHOICES = [
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
        ('compliment', 'Compliment'),
    ]
    
    CATEGORY_CHOICES = [
        ('dish', 'Dish'),
        ('service', 'Service'),
    ]
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=True, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, null=True, blank=True)
    want_to_reach_us = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True, null=True)  
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.vendor.name}"

class AndroidDevice(models.Model):
    token = models.CharField(max_length=255, unique=True)
    mac_address = models.CharField(max_length=255, blank=True, null=True,unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True, blank=True)
    admin_outlet = models.ForeignKey(AdminOutlet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
