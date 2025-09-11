
from fetch_rpi_metrics import get_cpu_temp,get_storage,get_runtime,get_network_traffic
from mqttHandler import MQTTPublisher
import time,json,datetime
from configs import config


publisher = MQTTPublisher(
        host=config.MQTT_BROKER_HOST,
        port=config.MQTT_BROKER_PORT,
        username=config.MQTT_BROKER_USERNAME,
        password=config.MQTT_BROKER_PASSWORD
    )
publisher.start()

while True:
    ts = str(datetime.datetime.now())

    data = {
        "cpu_temp": get_cpu_temp(),
        "storage_total": get_storage()[0],
        "storage_used": get_storage()[1],
        "storage_free": get_storage()[2],
        "runtime": get_runtime(),
        "upload_traffic": get_network_traffic()[0],
        "download_traffic": get_network_traffic()[1],
        "ts": ts
    }

    for key, value in data.items():
        payload = json.dumps({"value": value, "ts": ts})
        publisher.publish(payload, f"{key}",qos=1)

    time.sleep(config.BUFFER_TIME)


