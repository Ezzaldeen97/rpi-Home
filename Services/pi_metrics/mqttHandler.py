import paho.mqtt.client as paho
from paho import mqtt
from datetime import datetime
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils.logger import get_logger


logger = get_logger("mqtt_logger", file_name='logs/mqtt_publisher.log')


class MQTTPublisher:
    """
    MQTT Publisher class that manages MQTT client conenctions, 
    publishes messages to different topics
    """


    def __init__(self, host: str, port: int, username: str, password: str):
        """
        Initialize the MQTT Publisher client object.

        Args:
        -----
        host(str): MQTT broker hostname
        port(int): MQTT broker port number
        username(str): Username for MQTT broker authentication
        password(str): Password for MQTT broker authentication.



        """
        
        date_str = datetime.now().strftime("%d%m%y")
        client_id = f"RPI@Home"
        self.client = paho.Client(client_id=client_id, protocol=paho.MQTTv5)
        self.client.username_pw_set(username, password) #NOTE: username/password are not required but essential for HiveMQ
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.on_connect = self.on_connect
        self.client.will_set(topic="last well", payload="connection lost", qos=2)

        self.client.on_publish = self.on_publish
        self.client.on_disconnect=self.on_disconnect
        try:
            self.client.connect(host, port, keepalive=30)
            logger.info("Mqtt publisher it connected")
        except Exception as e :
            logger.error("Mqtt could not connect.")
            sys.exit(1)

    def on_connect(self,client,userdata,flags,reason_code, properties):
        logger.info(f"Connected Reason code: {reason_code}")
    def on_disconnect(self, client, userdata, reason_code, properties=None):
        logger.warning(f"Disconnected, Reason code: {reason_code}")
        retry_delay = 5 
        max_retries = 10

        for attempt in range(max_retries):
            try:
                logger.info(f"Trying to reconnect... attempt {attempt+1}/{max_retries}")
                client.reconnect()
                logger.info("Reconnected successfully")
                return
            except Exception as e:
                logger.error(f"Reconnect failed: {e}")
                time.sleep(retry_delay)

        logger.critical("Max reconnect attempts reached, giving up")

    def on_publish(self,client,userdata,mid):
        logger.info(f"Published mid: {mid}")

    def get_topic(self, topic)->str:
        """
        Determine MQTT topic based on sensor datapoint object
        
        Args:
        ----
        message(Datapoint|Datapoint_Nmea): Message object to publish
        
        Rerunts:
        --------
        str: The topic string of the message
        """

        return f"Pi/Stats/{topic}"

    def publish(self, message: str,topic, qos: int = 1):
        """
        Publish a message to the MQTT broker on appropriate topic

        Args:
        -----
        message(str): The message to publish

        qos(int, optional): Quality of service lever (deafult is 1 ) -> To fullfill the requirement that at least the message needs to be send once
        """
        
        
        self.topic = self.get_topic(topic)
        if True:
            logger.info(f"[Publishing] {message} to topic '{self.topic}'")
            self.client.publish(self.topic, payload=message, qos=qos)
        else:
            logger.info(f"Message {message} with topic {self.topic} cant be published as it didnt change or its invalid")

    def start(self):
        """
        Start the MQTT network loop.
        
        """
        logger.info("Starting MQTT loop")
        self.client.loop_start()