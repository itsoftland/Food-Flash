from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from vendors.models import AdminOutlet, Device, Vendor

@login_required
def dashboard(request):
    try:
        admin_outlet = request.user.admin_outlet 
    except:
        return redirect('/login')
    context = {
        'admin_outlet': admin_outlet
    }
    return render(request, 'company/dashboard.html', context)

from django.shortcuts import render, redirect
import json

def create_outlet(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        place_id = request.POST.get('place_id')
        device_mapping_id = request.POST.get('device_mapping')
        logo = request.FILES.get('logo')

        Vendor.objects.create(
            name=name,
            location=location,
            place_id=place_id,
            logo=logo,
            device_mapping_id=device_mapping_id if device_mapping_id else None
        )
        return redirect('company:dashboard')

    # Assuming this JSON comes from DB or settings
    admin_outlet = request.user.admin_outlet
    locations_json = admin_outlet.locations
    locations_data = json.loads(locations_json)
    locations = [{'key': list(i.keys())[0], 'value': list(i.values())[0]} for i in locations_data]

    devices = Device.objects.all()
    return render(request, 'company/create_outlet.html', {
        'locations': locations,
        'devices': devices,
        'admin_outlet':admin_outlet
    })