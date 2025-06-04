from django.urls import path
from .import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('create-outlet/', views.create_outlet, name='create_outlet'),
    path('api/create_vendor/', views.create_vendor, name='create_vendor'),
]
