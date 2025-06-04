# middleware.py
from django.http import JsonResponse
from django.shortcuts import render
from vendors.models import SiteConfig

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            config = SiteConfig.objects.first()
            if config.maintenance_mode:
                if request.path.startswith('/api'):
                    return JsonResponse({
                        'status': 'maintenance',
                        'message': 'The system is under maintenance. Please try again shortly.'
                    }, status=503)
                return render(request, 'companyadmin/maintenance.html', status=503)
        except:
            pass  # On DB error, skip maintenance (optional safety)

        return self.get_response(request)
