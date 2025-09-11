import os
import shutil
import time, psutil

def get_cpu_temp():
    "Read the RPI CPU tempretuate"
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read().strip()) / 1000.0
        return f"{temp:.1f}'C"
    except Exception as e:
        return f"Error: {e}"


def get_storage():
    "Read the RPI Total, used, free Storage"
    total, used, free = shutil.disk_usage("/")
    return f"{total//(2**30)} GB"  ,f"{used//(2**30)} GB", f"{free//(2**30)} GB"


def get_runtime():
    "Get the runtime of the RPI"
    boot_time = psutil.boot_time()
    return  f"{round((time.time() - boot_time))} seconds"

def get_network_traffic():
    "Get the actual Network traffic (tx, rx)"
    with open("/sys/class/net/eth0/statistics/tx_bytes", "r") as f:
        upload_traffic = round(int(f.read().strip())/1000,2)
    with open("/sys/class/net/eth0/statistics/rx_bytes", "r") as f:
        download_traffic = round(int(f.read().strip())/1000,2)        
    return f"{upload_traffic} Kb", f"{download_traffic} Kb"
    
