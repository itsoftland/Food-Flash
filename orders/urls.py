from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Fetch order status (GET request)
    path('check-status/', views.check_status, name='check_status'),
]
