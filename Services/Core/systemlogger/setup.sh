#!/bin/bash

SCRIPT_NAME="logcli.py"
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"  
DEST_DIR="/usr/local/bin"
DEST_PATH="$DEST_DIR/logcli"

echo "Copying $SCRIPT_NAME to $DEST_DIR..."
sudo cp "$SRC_DIR/$SCRIPT_NAME" "$DEST_PATH"

sudo chmod +x "$DEST_PATH"
echo "Made $DEST_PATH executable"

export PYTHONPATH=$PYTHONPATH:$DEST_DIR
echo "Added $DEST_DIR to PYTHONPATH for current session"


echo "Setup complete! You can now run 'logcli' from anywhere and import it in Python."
