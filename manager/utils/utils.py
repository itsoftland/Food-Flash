# Food-Flash/manager/utils/utils.py

from rest_framework.exceptions import NotFound
def get_manager_vendor(user):
    profile = user.profile_roles.filter(role='manager').first()
    if not profile or not profile.vendor:
        raise NotFound("Vendor not found for this manager")
    return profile.vendor