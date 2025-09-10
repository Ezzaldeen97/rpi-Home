
from get_info import get_cpu_temp,get_storage,get_runtime,get_network_traffic
from mqttHandler import MQTTPublisher
import time,json,datetime

publisher = MQTTPublisher(
        host="a7fb406d74d6425f98e1bb4b6da01446.s1.eu.hivemq.cloud",
        port=8883,
        username="",
        password=""
    )
publisher.start()

while True:
    ts = str(datetime.datetime.now())

    data = {
        "cpu_temp": get_cpu_temp(),
        "storage_total": get_storage()[0],
        "storage_free": get_storage()[1],
        "storage_used": get_storage()[2],
        "runtime": get_runtime(),
        "upload_traffic": get_network_traffic()[0],
        "download_traffic": get_network_traffic()[1],
        "ts": ts
    }

    for key, value in data.items():
        payload = json.dumps({"value": value, "ts": ts})
        publisher.publish(payload, f"{key}",qos=1)

    time.sleep(60)

