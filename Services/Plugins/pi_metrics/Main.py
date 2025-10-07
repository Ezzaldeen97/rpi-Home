
from fetch_rpi_metrics import get_cpu_temp,get_storage,get_runtime,get_network_traffic,get_cpu_usage,get_memory_usage
import time,json,datetime
import os
from dotenv import load_dotenv
import sys
sys.path.append("/usr/local/bin")  
from logcli import log_message
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.abspath(os.path.join(BASE_DIR, ".env"))
load_dotenv(dotenv_path=ENV_PATH)
TOPIC = os.getenv("TOPIC")

log_message("info","test","file1.log")
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
        "memory_usage":get_memory_usage(),
        "cpu_usage":get_cpu_usage(),
        "ts": ts
    }

    for key, value in data.items():
        if key=="ts":
            continue
        payload = json.dumps({"value": float(value), "ts": ts})
        topic=f"{TOPIC}/{key}"
        try:
            os.system(f"mqtt {topic} '{payload}'")
            log_message("INFO", f"message was successfully sent with topic :{topic} and payload {payload}", "pi-metrics-service.log")
        except Exception as e:
            log_message("WARNING", f"message was not sent with topic :{topic} and payload {payload} -> Error: {e}", "pi-metrics-service.log")


    time.sleep(int(os.getenv("BUFFER_TIME")))


