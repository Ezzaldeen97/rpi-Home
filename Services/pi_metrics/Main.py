
from fetch_rpi_metrics import get_cpu_temp,get_storage,get_runtime,get_network_traffic
from mqttHandler import MQTTPublisher
import time,json,datetime
import os
from dotenv import load_dotenv

load_dotenv()

publisher = MQTTPublisher(
        host=os.getenv("MQTT_BROKER_HOST"),
        port=os.getenv("MQTT_BROKER_PORT"),
        username=os.getenv("MQTT_BROKER_USERNAME"),
        password=os.getenv("MQTT_BROKER_PASSWORD")
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
        if key=="ts":
            continue
        payload = json.dumps({"value": float(value), "ts": ts})
        publisher.publish(payload, f"{key}",qos=1)

    time.sleep(os.getenv(BUFFER_TIME))


