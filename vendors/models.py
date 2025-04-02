from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    place_id = models.CharField(max_length=255, blank=True, null=True)
    vendor_id = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.vendor_id)

class Device(models.Model):
    serial_no = models.CharField(max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="devices")
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
    token_no = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preparing')
    counter_no = models.IntegerField(default=1)
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
