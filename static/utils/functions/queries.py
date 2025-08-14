from vendors.models import Vendor,Order
from .utils import (get_vendor_business_day_range,
                    get_vendor_current_date)

import logging
logger = logging.getLogger(__name__)

def get_vendor(vendor_id):
    return Vendor.objects.get(vendor_id=vendor_id)
 
# def get_order(token_no, vendor):
#     start_dt, end_dt = get_vendor_business_day_range(vendor)
#     return Order.objects.filter(
#         token_no=token_no,
#         vendor=vendor,
#         created_at__range=(start_dt, end_dt)
#     ).first()
    
def get_order(token_no, vendor):
    start_dt, end_dt = get_vendor_business_day_range(vendor)
    order = Order.objects.filter(
        token_no=token_no,
        vendor=vendor,
        created_at__range=(start_dt, end_dt)
    ).first()

    if not order:
        order = Order.objects.create(
            token_no=token_no,
            vendor=vendor,
            status='ready',  # default status
            created_at=get_vendor_current_date(vendor),
        )
    return order



def update_existing_order_by_manager(token_no, vendor, device, status,manager):
    order = get_order(token_no, vendor)
    if order:
        order.status = status
        order.updated_by = "manager"
        order.device = device
        order.user_profile = manager
        order.save()
    return order

