#!/bin/bash
# Simple MQTT publish CLI with .env support

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"
# Load .env if available
if [ -f "$ENV_FILE" ]; then
  set -a
  . "$ENV_FILE"
  set +a
fi

TOPIC=$1
PAYLOAD=$2

if [ -z "$TOPIC" ] || [ -z "$PAYLOAD" ]; then
  echo "Usage: mqtt <topic> <payload>"
  exit 1
fi

/usr/bin/mosquitto_pub \
  -h "$MQTT_BROKER_HOST" \
  -p "$MQTT_BROKER_PORT" \
  -u "$MQTT_BROKER_USERNAME" \
  -P "$MQTT_BROKER_PASSWORD" \
  -t "$TOPIC" \
  -m "$PAYLOAD"
