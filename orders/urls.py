from django.urls import path
from .import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.outlet_selection, name="outlet_selection"),
    path('check-status/', views.check_status, name='check_status'),
    path('api/outlets/', views.get_outlets, name="get_outlets"),
    path('api/get_vendor_logos/', views.get_vendor_logos, name='get_vendor_logos'),
]
