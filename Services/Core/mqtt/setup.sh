#!/bin/bash
set -e

SERVICE_NAME="mqtt-core"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[1/3] Installing mosquitto clients..."
sudo apt-get update -y
sudo apt-get install -y mosquitto mosquitto-clients

echo "[2/3] Copying CLI script..."
sudo cp "$SCRIPT_DIR/mqtt-cli.sh" /usr/local/bin/mqtt

sudo chmod +x /usr/local/bin/mqtt

echo "[2.5/3] Setting up .env..."
if [ ! -f "$SCRIPT_DIR/.env" ]; then
  cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
  sudo cp "$SCRIPT_DIR/.env" /usr/local/bin/mqtt/.env
  echo "✅ Copied .env.example → .env"
fi
sudo cp "$SCRIPT_DIR/.env" /usr/local/bin/.env

echo "[3/3] Setting up systemd service..."
sudo cp "$SCRIPT_DIR/mqtt-daemon.service" /etc/systemd/system/$SERVICE_NAME.service
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME.service
sudo systemctl restart $SERVICE_NAME.service

echo "✅ MQTT Core service and CLI installed."
