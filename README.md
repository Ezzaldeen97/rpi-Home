# rpi-Home


A modular Raspberry Pi IoT data logging system that collects metrics and sensor data, publishes them over MQTT, and can be visualized in real-time. 
Designed to be expandable with additional sensors and devices in the future.

---

## Features
- Monitor Raspberry Pi system metrics:
  - CPU temperature
  - Storage usage (total, free, used)
  - Network traffic (upload/download)
  - Uptime/runtime
  - Power consumption (planned)
- Publish metrics over MQTT to any broker (HiveMQ, Mosquitto, etc.)
- All metrics are published to MQTT topics

## How to run it
1. Clone the repo
2. Install dependencies (Recommended to create virtual env)
 ```
pip install requirements.txt
 ```
3. Configure the enviroment parameters in  ```config.py ``` file
4. Run the main script  ```python Main.py ```
5. Or run as systemd service 


## Future ideas
- Support physical sensors (tempreture, humidity,..etc)
- Connect to time-series database (pipeline)
- Connect the db to a dashboard.
- OTAU
- Telegram bots for alerts

