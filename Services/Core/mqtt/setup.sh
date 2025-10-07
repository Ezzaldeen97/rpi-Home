#!/bin/bash
set -e

INSTALL_DIR="/usr/local/bin/core"
BIN_DIR="/usr/local/bin"
USER_HOME=$(eval echo "~$SUDO_USER")

echo "Installing mqtt_client..."

sudo mkdir -p "$INSTALL_DIR"
echo  "[3/5] Setting up the environment "
if [ ! -f "$USER_HOME/mqtt.env" ]; then
  echo " Copying .env.example to $USER_HOME/.mqtt.env "
cp "$(dirname "$0")/.env" "$USER_HOME/.mqtt.env"
fi
# Copy the Python file
sudo cp "$(dirname "$0")/mqtt_client.py" "$INSTALL_DIR/"

# Create a symlink for CLI
sudo ln -sf "$INSTALL_DIR/mqtt_client.py" "$BIN_DIR/mqtt"

# Make it executable
sudo chmod +x "$INSTALL_DIR/mqtt_client.py"
sudo chmod +x "$BIN_DIR/mqtt"

echo "✅ mqtt_client installed!"
echo "   CLI available as: mqtt"
echo "   Importable as: from mqtt_client import MQTTPublisher"
echo
echo "⚙️  To configure MQTT globally, export environment variables:"
echo "   export MQTT_BROKER_HOST='your-broker'"
echo "   export MQTT_BROKER_PORT=8883"
echo "   export MQTT_BROKER_USERNAME='user'"
echo "   export MQTT_BROKER_PASSWORD='pass'"
echo
echo "   Add them permanently to ~/.bashrc or /etc/environment if needed."
