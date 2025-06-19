from django.urls import path
from .import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('banners/', views.banners, name='banners'), 
    path('outlets/', views.outlets, name='outlets'),
    path('create-outlet/', views.create_outlet, name='create_outlet'),
    path('update_outlet/', views.update_outlet_page, name='update_outlet_page'),
    path('configurations/', views.configurations, name='configurations'), 
    path('api/create_vendor/', views.create_vendor, name='create_vendor'),
    path('api/update_vendor/', views.update_vendor, name='update_vendor'),
    path('api/get_vendors/', views.get_vendors, name='get_vendors'),
    path('api/banner_upload/', views.upload_banner, name='upload_banner'),
    path('api/banner_list/', views.list_banners, name='list_banners'),
    path('api/banner_delete/', views.delete_banner, name='delete_banner'),
    path('api/get_vendor_details/', views.get_vendor_details, name='get_vendor_details'),
    path('api/get_outlet_creation_data/', views.get_outlet_creation_data, name='get_outlet_creation_data'),
]
 