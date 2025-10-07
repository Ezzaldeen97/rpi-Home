import os,sys
import shutil
import time, psutil

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
sys.path.append("/usr/local/bin")  
from logcli import log_message


def get_cpu_temp():
    "Read the RPI CPU temperature"
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read().strip()) / 1000.0
        return f"{temp:.1f}"
    except Exception as e:
        log_message("WARNING", f"Could not read the cpu temperature: {e}", "pi-metrics-service.log")
        


def get_storage():
    #TODO: Handle errors
    "Read the RPI Total, used, free Storage"
    total, used, free = shutil.disk_usage("/")
    return f"{total//(2**30)}"  ,f"{used//(2**30)} ", f"{free//(2**30)}"


def get_runtime():
    #TODO: Handle errors
    "Get the runtime of the RPI"
    boot_time = psutil.boot_time()
    return  f"{round((time.time() - boot_time))} "

def get_network_traffic():
    #TODO: Handle errors
    "Get the actual Network traffic (tx, rx)"
    with open("/sys/class/net/eth0/statistics/tx_bytes", "r") as f:
        upload_traffic = round(int(f.read().strip())/1000,2)
    with open("/sys/class/net/eth0/statistics/rx_bytes", "r") as f:
        download_traffic = round(int(f.read().strip())/1000,2)        
    return f"{upload_traffic}", f"{download_traffic} "
    
def get_cpu_usage():
    cpu = psutil.cpu_percent()
    return cpu

def get_memory_usage():
    memory= psutil.virtual_memory().percent
    return memory