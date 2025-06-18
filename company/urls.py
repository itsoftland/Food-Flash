from django.urls import path
from .import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('outlets/', views.outlets, name='outlets'),
    path('create-outlet/', views.create_outlet, name='create_outlet'),
    path('configurations/', views.configurations, name='configurations'), 
    path('api/create_vendor/', views.create_vendor, name='create_vendor'),
    path('api/update_vendor/', views.update_vendor, name='update_vendor'),
    path('api/get_vendors/', views.get_vendors, name='get_vendors'),
    path('update_outlet/', views.update_outlet_page, name='update_outlet_page'),
    path('api/get_vendor_details/', views.get_vendor_details, name='get_vendor_details'),
    path('api/get_outlet_creation_data/', views.get_outlet_creation_data, name='get_outlet_creation_data'),
]
 