#!/usr/bin/with-contenv bashio

echo "Starting Household Chores!"

MQTT_HOST=$(bashio::services mqtt "host")
MQTT_USER=$(bashio::services mqtt "username")
MQTT_PASSWORD=$(bashio::services mqtt "password")
MQTT_PORT=$(bashio::services mqtt "port")

export MQTT_HOST
export MQTT_USER
export MQTT_PASSWORD
export MQTT_PORT

CONFIG_PATH=/data/options.json

export CONFIG_PATH

source .venv/bin/activate
python3 -u start.py