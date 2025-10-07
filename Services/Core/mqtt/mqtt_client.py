#!/usr/bin/env python3
import os
import sys
import paho.mqtt.client as paho
from paho import mqtt
from dotenv import load_dotenv

ENV_FILE = os.path.expanduser("~/.mqtt.env")
print(ENV_FILE)
load_dotenv(dotenv_path=ENV_FILE)

sys.path.append("/usr/local/bin")  
from logcli import log_message

# Read from system environment (no .env required)
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
MQTT_BROKER_USERNAME = os.getenv("MQTT_BROKER_USERNAME", "")
MQTT_BROKER_PASSWORD = os.getenv("MQTT_BROKER_PASSWORD", "")
print(MQTT_BROKER_HOST)

LOG_FILE = "mqtt_client.log"


class MQTTPublisher:
    """Reusable MQTT publisher that connects only when needed."""

    def __init__(self, host=MQTT_BROKER_HOST, port=MQTT_BROKER_PORT, 
                 username=MQTT_BROKER_USERNAME, password=MQTT_BROKER_PASSWORD):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        """Establish MQTT connection."""
        if not all([self.host, self.port, self.username, self.password]):
            raise ValueError("MQTT Publisher must be initialized with host, port, username, and password")

        client_id = f"ows-challenge"
        self.client = paho.Client(client_id=client_id, protocol=paho.MQTTv5)
        self.client.username_pw_set(self.username, self.password)
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.will_set(topic="last/will", payload="connection lost", qos=2)

        try:
            self.client.connect(self.host, self.port, keepalive=30)
            self.client.loop_start()
            log_message("info", "MQTT connected", LOG_FILE)
        except Exception as e:
            log_message("error", f"MQTT connection failed: {e}", LOG_FILE)
            sys.exit(1)

    def disconnect(self):
        """Cleanly disconnect."""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            log_message("info", "MQTT disconnected", LOG_FILE)

    def on_connect(self, client, userdata, flags, reason_code, properties):
        log_message("info", f"Connected. Reason code: {reason_code}", LOG_FILE)

    def on_disconnect(self, client, userdata, reason_code, properties):
        log_message("info", f"Disconnected. Reason code: {reason_code}", LOG_FILE)

    def on_publish(self, client, userdata, mid):
        log_message("info", f"Published mid: {mid}", LOG_FILE)

    def publish(self, topic: str, message: str, qos: int = 1):
        """Connect, publish, and disconnect each time."""
        self.connect()
        log_message("info", f"[Publishing] {message} to topic '{topic}'", LOG_FILE)
        self.client.publish(topic, payload=message, qos=qos)
        self.disconnect()


def main():
    if len(sys.argv) < 3:
        print("Usage: mqtt <topic> <payload>")
        sys.exit(1)
    topic = sys.argv[1]
    payload = sys.argv[2]
    mqtt_client = MQTTPublisher()
    mqtt_client.publish(topic, payload)
    print(f"Published to {topic}: {payload}")


if __name__ == "__main__":
    main()
