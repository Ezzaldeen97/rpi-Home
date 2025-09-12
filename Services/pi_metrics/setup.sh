#! /bin/bash
set -e
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_DIR=$(pwd)
SERVICE_NAME=pi_metrics
SERVICE_PATH=$PROJECT_DIR/Services/$SERVICE_NAME
SERVICE_FILE=/etc/systemd/system/${SERVICE_NAME}.service

echo  "${RED}==========================Running ${SERVICE_NAME}==========================${NC}"

echo  "${RED}[1/5] Updating system packages.....${NC}"

sudo apt-get update -y
sudo apt-get upgrade -y
echo  "${GREEN} System packages updated ${NC}"

echo  "${RED}[2/5] Installing python and pip ....${NC}"

sudo apt-get install -y python3 python3-venv python3-pip

echo  "${GREEN} Python and pip are updated ${NC}"

echo  "${RED}[3/5] Setting up the enviroments ${NC}"


echo  "${RED}[4/5] Setting up pi metrics service ${NC}"

cd $SERVICE_PATH
python3 -m venv venv

venv/bin/python -m pip install -r requirements.txt
cd $PROJECT_DIR
echo  "${GREEN} Python dependencies are installed ${NC}"

echo  "${RED}[5/5] creating systemd service for ${SERVICE_NAME} ${NC}"
sudo tee $SERVICE_FILE > /dev/null <<EOL
[Unit] 

Description=Pi Metrics Publisher 

After=network.target 

[Service]
ExecStart=/usr/bin/python3 ${SERVICE_PATH}/Main.py 
WorkingDirectory=${PROJECT_DIR} 
StandardOutput=journal 
StandardError=journal 
Restart=always 
User=ezz

[Install] 
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reexec
sudo systemctl enable ${SERVICE_NAME}.service
sudo systemctl restart ${SERVICE_NAME}.service

echo "${GREEN}== Setup Complete, ${SERVICE_NAME} is now running as a service. ==${NC}"
echo "${GREEN} Check logs with: sudo journalctl -u ${SERVICE_NAME} -f ${NC}"