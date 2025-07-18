"""
URL configuration for caller_on project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vendors/', include(('vendors.urls','vendors'),namespace='vendors')),
    path('company/', include(('company.urls', 'company'), namespace='company')),
    path('companyadmin/', include(('companyadmin.urls', 'companyadmin'), namespace='companyadmin')),
    path('',include('orders.urls')),
    path('manager/', include(('manager.urls','manager'),namespace='manager')),
    path('service-worker.js', (TemplateView.as_view(template_name="orders/service-worker.js", 
  content_type='application/javascript', )), name='service-worker.js'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
