from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Fetch order status (GET request)
    path('check-status/', views.check_status, name='check_status'),
    path('outlets/', views.outlet_selection, name="outlet_selection"),
    path('api/outlets/', views.get_outlets, name="get_outlets"),
    path('api/get_vendor_logos/', views.get_vendor_logos, name='get_vendor_logos'),
]
