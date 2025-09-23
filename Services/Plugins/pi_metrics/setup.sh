#!/bin/bash
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
# Directories
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
SERVICE_NAME=pi_metrics
SERVICE_PATH=$SCRIPT_DIR
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

# Logging
LOG_DIR="$SERVICE_PATH/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/setup_${SERVICE_NAME}_$(date +%Y%m%d_%H%M%S).log"

# exec > >(tee -a "$LOG_FILE") 2>&1

echo  "${RED}========================== Running ${SERVICE_NAME} ==========================${NC}"

echo  "${RED}[1/5] Updating system packages.....${NC}"
sudo apt-get update -y && sudo apt-get upgrade -y
echo  "${GREEN} System packages updated ${NC}"

echo  "${RED}[2/5] Installing python and pip ....${NC}"
sudo apt-get install -y python3 python3-venv python3-pip
echo  "${GREEN} Python and pip are installed ${NC}"

echo  "${RED}[3/5] Setting up the environment ${NC}"
if [ ! -f "$SERVICE_PATH/.env" ]; then
  echo "${RED} Copying .env.example to .env ${NC}"
  cp "$SERVICE_PATH/.env.example" "$SERVICE_PATH/.env"
fi

echo  "${RED}[4/5] Setting up ${SERVICE_NAME} service ${NC}"
cd "$SERVICE_PATH"
python3 -m venv venv
venv/bin/pip install -r requirements.txt
cd "$PROJECT_DIR"
echo  "${GREEN} Python dependencies are installed ${NC}"

echo  "${RED}[5/5] Creating systemd service for ${SERVICE_NAME} ${NC}"
CURRENT_USER=$(whoami)
sudo tee "$SERVICE_FILE" > /dev/null <<EOL
[Unit]
Description=Pi Metrics Publisher
After=network.target

[Service]
ExecStart=${SERVICE_PATH}/venv/bin/python ${SERVICE_PATH}/Main.py
WorkingDirectory=${PROJECT_DIR}
StandardOutput=journal
StandardError=journal
Restart=always
User=${CURRENT_USER}

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl enable "${SERVICE_NAME}.service"
sudo systemctl restart "${SERVICE_NAME}.service"

echo "${GREEN}== Setup Complete, ${SERVICE_NAME} is now running as a service. ==${NC}"
echo "${GREEN} Check logs with: sudo journalctl -u ${SERVICE_NAME} -f ${NC}"
