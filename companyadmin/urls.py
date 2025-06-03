from django.urls import path
from .import views

urlpatterns = [
    path('api/register-company/', views.register_company, name='register-company'),
    path('registration/', views.registration, name='registration'),
    path('api/product-registrations/', views.product_registration, name='product-registration'),
    path('api/product-authentications/', views.product_authentication, name='product-authentication'),
    # path('token_display/',views.token_display,name='token_display'),
    # path('login/', views.login_view, name='loginview'), 
    # path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('company_dashboard/', views.company_dashboard, name='company_dashboard'), 
    # path('outlet_dashboard/', views.outlet_dashboard, name='outlet_dashboard'),
    # path('api/company-update/', views.update_admin_outlet, name='company_update_api'),
    # path('create-outlet/', views.create_outlet, name='create_outlet'),
]
