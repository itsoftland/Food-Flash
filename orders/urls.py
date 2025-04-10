from django.urls import path
from .import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.outlet_selection, name="outlet_selection"),
    path('check-status/', views.check_status, name='check_status'),
    path('api/outlets/', views.get_outlets, name="get_outlets"),
    path('api/get_vendor_logos/', views.get_vendor_logos, name='get_vendor_logos'),
    path('api/get_vendor_ads/', views.get_vendor_ads, name='get_vendor_ads'),
    path('api/menus/', views.get_vendor_menus, name='get_vendor_menu'),
    path('api/submit_feedback/', views.submit_feedback, name='submit-feedback'),
]
