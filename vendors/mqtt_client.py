# utils/mqtt_client.py
import json
import logging
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)
# vendors/utils.py

def get_mqtt_config_for_vendor(vendor):
    """
    Returns MQTT configuration dictionary for a given Vendor instance.
    If no configuration is found, returns an empty dict.
    """
    if not vendor:
        return {}
    admin_outlet = getattr(vendor, "admin_outlet", None)
    mqtt_server = getattr(admin_outlet, "mqtt_server", None) if admin_outlet else None
    return {
        "topic": f"FF/{vendor.vendor_id}/ALL",
        "host": mqtt_server.host if mqtt_server else None,
        "port": mqtt_server.port if mqtt_server else None,
        "username": mqtt_server.username if mqtt_server else None,
        "password": mqtt_server.password if mqtt_server else None,
        "qos": mqtt_server.qos if mqtt_server else None
    }

def publish_mqtt(vendor,topic, payload):
    """
    Publish a payload to the vendor's MQTT broker and topic.
    Vendor must have an MQTT server configured.
    """
    cfg = get_mqtt_config_for_vendor(vendor)

    if not cfg.get("host") or not cfg.get("topic"):
        logger.error(f"🚨 No valid MQTT configuration found for vendor: {vendor}")
        return

    try:
        logger.info(f"📡 Connecting to MQTT Broker {cfg['host']}:{cfg['port']}")
        client = mqtt.Client()

        if cfg.get("username") and cfg.get("password"):
            client.username_pw_set(cfg["username"], cfg["password"])
            logger.debug(f"🔑 Using MQTT authentication for user '{cfg['username']}'")

        client.connect(cfg["host"], cfg["port"], 60)
        logger.info(f"📤 Publishing to topic: {topic} | QoS: {cfg['qos']}")
        logger.debug(f"Payload: {json.dumps(payload)}")

        result = client.publish(topic, json.dumps(payload), qos=cfg["qos"])

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            logger.info("✅ MQTT message published successfully")
        else:
            logger.error(f"❌ MQTT publish failed with code: {result.rc}")

    except Exception as e:
        logger.exception(f"🚨 MQTT publish error: {e}")
    finally:
        try:
            client.disconnect()
            logger.debug("🔌 Disconnected from MQTT broker")
        except Exception as e:
            logger.warning(f"⚠️ Error while disconnecting MQTT: {e}")

