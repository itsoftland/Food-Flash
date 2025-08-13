# vendors/services/order_service.py
import logging
from vendors.mqtt_client import publish_mqtt
from vendors.order_utils import get_last_tokens

logger = logging.getLogger(__name__)

def send_order_update(vendor):
    """Send an MQTT update with the latest order tokens for a vendor.

    Args:
        vendor: The vendor object containing vendor details and configuration.
    """
    config = vendor.config
    tokens = get_last_tokens(vendor, config.token_display_limit)
    total_count = total_count = len(tokens)

    payload = {
        "vendor_id": vendor.vendor_id,
        "mode": config.mqtt_mode,
        "total_count": total_count,
        "tokens": tokens
    }

    logger.info(f"📡 Sending MQTT update | Vendor: {vendor.name} (ID: {vendor.vendor_id}) | Mode: {config.mqtt_mode} | Total Orders: {total_count}")
    logger.debug(f"Payload: {payload}")

    if config.mqtt_mode == "All":
        # topic = f"FF/{vendor.vendor_id}/ALL"
        # logger.info(f"→ Topic: {topic}")
        publish_mqtt(vendor,payload)

    elif config.mqtt_mode == "Individual":
        for device in vendor.devices.all():
            # topic = f"FF/{vendor.vendor_id}/{device.device_id}"
            # logger.info(f"→ Topic: {topic} (Device: {device.device_id})")
            publish_mqtt(vendor, payload)

    elif config.mqtt_mode == "Keypad":
        for device in vendor.devices.all():
            # topic = f"foodflash/vendor/{vendor.vendor_id}/keypad/{device.label}"
            # logger.info(f"→ Topic: {topic} (Keypad Label: {device.label})")
            publish_mqtt(vendor, payload)

    
