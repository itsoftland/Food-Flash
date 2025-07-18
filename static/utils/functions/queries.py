from vendors.models import Vendor,Order
from django.utils import timezone

import logging
logger = logging.getLogger(__name__)

def get_vendor(vendor_id):
    return Vendor.objects.get(vendor_id=vendor_id)

def get_order(token_no, vendor):
    today = timezone.localdate()
    return Order.objects.filter(
        token_no=token_no,
        vendor=vendor,
        created_date=today
    ).first()


def update_existing_order_by_manager(token_no, vendor, device, status,manager):
    order = get_order(token_no, vendor)
    if order:
        logger.info(f"Updating existing order {token_no}")
        order.status = status
        order.updated_by = "manager"
        order.device = device
        order.user_profile = manager
        order.save()
    return order

