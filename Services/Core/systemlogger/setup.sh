#!/bin/bash
set -e

INSTALL_DIR="/usr/local/bin/core"
BIN_DIR="/usr/local/bin"

echo "Installing systemlogger..."

sudo mkdir -p "$INSTALL_DIR"

# Copy the Python file
sudo cp "$(dirname "$0")/logcli.py" "$INSTALL_DIR/"

# Create a symlink so it can be used as CLI
sudo ln -sf "$INSTALL_DIR/logcli.py" "$BIN_DIR/logcli"

# Make sure it’s executable
sudo chmod +x "$INSTALL_DIR/logcli.py"
sudo chmod +x "$BIN_DIR/logcli"

echo "✅ systemlogger installed!"
echo "   - CLI available as: logcli"
echo "   - Importable in Python via:"
echo "       sys.path.append('/usr/local/lib/core')"
echo "       from logcli import log_message"
