from django.urls import path
from .import views

urlpatterns = [
    path('api/create_order/', views.create_order_by_manager,name='create_order_by_manager'),
    path('api/get_today_orders/', views.get_today_orders, name='get_today_orders'),
    path('api/manager_order_update/', views.manager_order_update, name='manager_order_update'),
    path('api/chat_history/',views.chat_history,name='chat_history'),
    path('api/device_call/', views.device_call, name='device_call'),
]
