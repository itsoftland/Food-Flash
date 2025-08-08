# utils/mqtt_client.py
import json
import logging
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_USERNAME = ""
MQTT_PASSWORD = ""
MQTT_QOS = 2  # Exactly once

def publish_mqtt(topic, payload):
    try:
        logger.info(f"📡 Connecting to MQTT Broker {MQTT_BROKER}:{MQTT_PORT}")
        client = mqtt.Client()

        if MQTT_USERNAME and MQTT_PASSWORD:
            client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
            logger.debug(f"🔑 Using MQTT authentication for user '{MQTT_USERNAME}'")

        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        logger.info(f"📤 Publishing to topic: {topic} | QoS: {MQTT_QOS}")
        logger.debug(f"Payload: {json.dumps(payload)}")

        result = client.publish(topic, json.dumps(payload), qos=MQTT_QOS)

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
