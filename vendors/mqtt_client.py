# vendors/mqtt_client.py
import json
import ssl
import time
import logging
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)


def get_mqtt_topic(vendor, device=None):
    """
    Generates MQTT topic dynamically based on vendor's MQTT mode.
    
    Args:
        vendor: Vendor object with config
        device: Optional device object (for Individual)
    
    Returns:
        str: Formatted topic string
    """
    if not vendor or not hasattr(vendor, 'config'):
        return None
        
    mode = getattr(vendor.config, 'mqtt_mode', 'All')
    
    if mode == "All":
        return f"FF/{vendor.vendor_id}/ALL"
    elif mode == "Individual" and device:
        return f"FF/{vendor.vendor_id}/{device.device_id}"
    elif mode == "Keypad" and device:
        return f"foodflash/vendor/{vendor.vendor_id}/keypad/{device.label}"
    else:
        logger.warning(f"Invalid MQTT mode or missing device: {mode}")
        return None
    
def get_mqtt_config_for_vendor(vendor, device=None):
    """
    Returns MQTT configuration dictionary for a given Vendor instance.
    If no configuration is found, returns an empty dict.
    """
    if not vendor:
        return {}
    admin_outlet = getattr(vendor, "admin_outlet", None)
    mqtt_server = getattr(admin_outlet, "mqtt_server", None) if admin_outlet else None
    return {
        "topic": get_mqtt_topic(vendor, device),
        "host": mqtt_server.host if mqtt_server else None,
        "port": mqtt_server.port if mqtt_server else None,
        "username": mqtt_server.username if mqtt_server else None,
        "password": mqtt_server.password if mqtt_server else None,
        "qos": mqtt_server.qos if mqtt_server else None,
        "tls": getattr(mqtt_server, "tls", False) if mqtt_server else False
    }

# def publish_mqtt(vendor,payload):
#     cfg = get_mqtt_config_for_vendor(vendor)

#     if not cfg.get("host") or not cfg.get("topic"):
#         logger.error(f"🚨 No valid MQTT configuration found for vendor: {vendor}")
#         return

#     try:
#         logger.info(f"📡 Connecting to MQTT Broker {cfg['host']}:{cfg['port']}")
#         client = mqtt.Client()

#         # Authentication
#         if cfg.get("username") and cfg.get("password"):
#             client.username_pw_set(cfg["username"], cfg["password"])
#             logger.debug(f"🔑 Using MQTT authentication for user '{cfg['username']}'")

#         # TLS setup if needed
#         if int(cfg["port"]) == 8883:
#             logger.info("🔐 Enabling TLS for secure MQTT connection")
#             client.tls_set(
#                 ca_certs="/etc/ssl/certs/ca-certificates.crt",
#                 certfile=None,
#                 keyfile=None,
#                 cert_reqs=ssl.CERT_REQUIRED,
#                 tls_version=ssl.PROTOCOL_TLS,
#                 ciphers=None
#             )
#             client.tls_insecure_set(False)

#         # Connect first, then start loop
#         client.connect(cfg["host"], int(cfg["port"]), 60)
#         client.loop_start()

#         logger.info(f"📤 Publishing to topic: {cfg['topic']} | QoS: {cfg['qos']}")
#         logger.debug(f"Payload: {json.dumps(payload)}")

#         result = client.publish(cfg.get("topic"), json.dumps(payload), qos=int(cfg["qos"]))
#         result.wait_for_publish()

#         if result.rc == mqtt.MQTT_ERR_SUCCESS:
#             logger.info("✅ MQTT message published successfully")
#         else:
#             logger.error(f"❌ MQTT publish failed with code: {result.rc}")

#     except Exception as e:
#         logger.exception(f"🚨 MQTT publish error: {e}")
#     finally:
#         try:
#             client.loop_stop()
#             client.disconnect()
#             logger.debug("🔌 Disconnected from MQTT broker")
#         except Exception as e:
#             logger.warning(f"⚠️ Error while disconnecting MQTT: {e}")

mqtt_clients = {}  # cache per vendor to keep persistent connections

def get_or_create_client(cfg):
    key = f"{cfg['host']}:{cfg['port']}:{cfg.get('username')}"
    if key in mqtt_clients and mqtt_clients[key].is_connected():
        return mqtt_clients[key]
    
    client = mqtt.Client(protocol=mqtt.MQTTv5)
    
    if cfg.get("username") and cfg.get("password"):
        client.username_pw_set(cfg["username"], cfg["password"])
    
    if int(cfg["port"]) == 8883 or cfg.get("tls"):
        client.tls_set(
            ca_certs="/etc/ssl/certs/ca-certificates.crt",
            certfile=None,
            keyfile=None,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLS,
            ciphers=None
        )
        client.tls_insecure_set(False)
    
    client.connect(cfg["host"], int(cfg["port"]), 60)
    client.loop_start()

    mqtt_clients[key] = client
    return client

def publish_mqtt(vendor, payload):
    cfg = get_mqtt_config_for_vendor(vendor)

    if not cfg.get("host") or not cfg.get("topic"):
        logger.error(f"No valid MQTT configuration for vendor: {vendor}")
        return

    try:
        client = get_or_create_client(cfg)

        logger.info(f"Publishing to {cfg['topic']} (QoS={cfg['qos']})")
        client.publish(cfg["topic"], json.dumps(payload), qos=int(cfg["qos"]), retain=False)

    except Exception as e:
        logger.exception(f"MQTT publish error: {e}")
