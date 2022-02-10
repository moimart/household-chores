from config import config
from time import gmtime, strftime
import paho.mqtt.client as mqtt
import json

class MQTTClient:
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        self.client.publish("kikkei/household/garbage", "ON")

        self.client.publish(config["mqtt_topic_next"], json.dumps(config["mqtt_payload_next"]), retain=True)
        self.client.publish(config["mqtt_topic_next_date"], json.dumps(config["mqtt_payload_next_date"]), retain=True)

    def on_message(self, client, userdata, msg):
        if self.delegate != None:
            self.delegate.on_message(msg.topic, msg.payload)

    def update_garbage(self, events):
        self.client.publish("kikkei/household/garbage/next", events[0].get("garbage"),retain=True)
        self.client.publish("kikkei/household/garbage/next_date", events[0].get("when"),retain=True)

        if len(events) > 1:
            self.client.publish("kikkei/household/garbage/nextafter", events[1].get("garbage"))
            self.client.publish("kikkei/household/garbage/nextafter_date", events[1].get("when"))

    def __init__(self):
        self.client = mqtt.Client()

        self.client.username_pw_set(
            config["hass_username"], password=config["hass_pwd"])

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(config["mqtt_host"], config["mqtt_port"], 60)
        self.delegate = None

    def loop(self):
        self.client.loop()