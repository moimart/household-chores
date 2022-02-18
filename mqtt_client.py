from devices import garbage_config
import paho.mqtt.client as mqtt
import json
from timer import Timer

class MQTTClient:
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        self.client.publish("kikkei/household/garbage", "ON")

        self.client.publish(garbage_config["mqtt_topic_next"], json.dumps(garbage_config["mqtt_payload_next"]), retain=True)
        self.client.publish(garbage_config["mqtt_topic_next_date"], json.dumps(garbage_config["mqtt_payload_next_date"]), retain=True)

    def on_disconnect(self, client, userdata, rc):
        self.timer.reset()
        self.timer.active = True

    def on_message(self, client, userdata, msg):
        if self.delegate != None:
            self.delegate.on_message(msg.topic, msg.payload)

    def update_garbage(self, events):
        if len(events) == 0:
            return

        self.client.publish("kikkei/household/garbage/next", events[0].get("garbage"),retain=True)
        self.client.publish("kikkei/household/garbage/next_date", events[0].get("when"),retain=True)

        if len(events) > 1:
            self.client.publish("kikkei/household/garbage/nextafter", events[1].get("garbage"))
            self.client.publish("kikkei/household/garbage/nextafter_date", events[1].get("when"))

    def __init__(self, username, password, host, port):
        self.client = mqtt.Client()

        self.client.username_pw_set(username, password)

        self.host = host
        self.port = port
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(host, port, 60)
        self.delegate = None
        self.timer = Timer(60, self)
        self.timer.active = False

    def on_timer(self, timer, elapsed):
        self.client.connect(self.host, self.port, 60)

    def step(self, dt):
        self.client.loop()
        self.timer.step(dt)