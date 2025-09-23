#!/bin/bash
set -e

SERVICE_NAME="mqtt-core"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[1/2] Installing mosquitto clients..."
sudo apt-get update -y
sudo apt-get install -y mosquitto mosquitto-clients

echo "[1.5/2] Copying CLI script..."
sudo cp "$SCRIPT_DIR/mqtt-cli.sh" /usr/local/bin/mqtt

sudo chmod +x /usr/local/bin/mqtt

echo "[2/2] Setting up .env..."
if [ ! -f "$SCRIPT_DIR/.env" ]; then
  cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
  sudo cp "$SCRIPT_DIR/.env" /usr/local/bin/mqtt/.env
  echo "✅ Copied .env.example → .env"
fi
sudo cp "$SCRIPT_DIR/.env" /usr/local/bin/.env

echo "✅ MQTT Core service and CLI installed."
