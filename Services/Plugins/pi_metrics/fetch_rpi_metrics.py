import os,sys
import shutil
import time, psutil
import sys
sys.path.append("/usr/local/bin/core")  
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from logcli import log_message
LOG_FILE ="pi-metrics-service.log"

def get_cpu_temp():
    """Read the RPI CPU temperature"""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read().strip()) / 1000.0
            log_message("INFO", f"Read CPU temperature: {temp:.1f}°C", LOG_FILE)
            return f"{temp:.1f}"
    except Exception as e:
        log_message("WARNING", f"Could not read CPU temperature: {e}", LOG_FILE)
        return None

def get_storage():
    """Read the RPI total, used, free storage in GB"""
    try:
        total, used, free = shutil.disk_usage("/")
        total_gb = total // (2**30)
        used_gb = used // (2**30)
        free_gb = free // (2**30)
        log_message("INFO", f"Storage - Total: {total_gb}GB, Used: {used_gb}GB, Free: {free_gb}GB", LOG_FILE)
        return str(total_gb), str(used_gb), str(free_gb)
    except Exception as e:
        log_message("WARNING", f"Could not read storage info: {e}", LOG_FILE)
        return None, None, None


def get_runtime():
    """Get the runtime of the RPI in seconds"""
    try:
        boot_time = psutil.boot_time()
        runtime = int(time.time() - boot_time)
        log_message("INFO", f"System runtime: {runtime}s", LOG_FILE)
        return str(runtime)
    except Exception as e:
        log_message("WARNING", f"Could not read system runtime: {e}", LOG_FILE)
        return None


def get_network_traffic():
    """Get the actual network traffic (tx_bytes, rx_bytes) in KB"""
    try:
        with open("/sys/class/net/eth0/statistics/tx_bytes", "r") as f:
            tx = round(int(f.read().strip()) / 1000, 2)
        with open("/sys/class/net/eth0/statistics/rx_bytes", "r") as f:
            rx = round(int(f.read().strip()) / 1000, 2)
        log_message("INFO", f"Network traffic - Upload: {tx}KB, Download: {rx}KB", LOG_FILE)
        return str(tx), str(rx)
    except Exception as e:
        log_message("WARNING", f"Could not read network traffic: {e}", LOG_FILE)
        return None, None

def get_cpu_usage():
    """Get the current CPU usage in %"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        log_message("INFO", f"CPU usage: {cpu_percent}%", LOG_FILE)
        return cpu_percent
    except Exception as e:
        log_message("WARNING", f"Could not read CPU usage: {e}", LOG_FILE)
        return None

def get_memory_usage():
    """Get the current memory usage in %"""
    try:
        memory_percent = psutil.virtual_memory().percent
        log_message("INFO", f"Memory usage: {memory_percent}%", LOG_FILE)
        return memory_percent
    except Exception as e:
        log_message("WARNING", f"Could not read memory usage: {e}", LOG_FILE)
        return None