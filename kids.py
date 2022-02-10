from posixpath import split
from config import kids, kids_device, hass_kid_entity, hass_kid_sensor
import json

class Kids:
    def __init__(self, mqtt):
        self.mqtt = mqtt
        self.mqtt.delegate = self
        self.kids = dict()

    def start(self):
        for kid in kids:
            self.create_kid(kid)

    def on_message(self, topic, payload):
        kid = topic.split("/")[2]
        kid = self.kids[kid]
        payload = payload.decode("utf-8")

        for switch in kid["switches"]:
            if switch["id"] == topic.split("/")[3]:
                if payload == 'ON':
                    print(switch["config"]["state_topic"])
                    self.mqtt.client.publish(switch["config"]["state_topic"], "true")
                elif payload == 'OFF':
                    self.mqtt.client.publish(switch["config"]["state_topic"], "false")
                else:
                    print("Unknown payload: {}".format(payload))
                return


    def create_kid(self, kid):
        topic = hass_kid_sensor["generic_sensor"]
        topic = topic.replace("#", kid["id"])

        config = hass_kid_sensor["generic_sensor_config"].copy()
        config["name"] = kid["name"]
        config["unique_id"] = "kid_" + kid["id"]
        config["state_topic"] = config["state_topic"].replace("#", kid["id"])

        self.mqtt.client.publish(config["state_topic"], 0)
        self.mqtt.client.publish(topic, json.dumps(config), retain=True)

        self.kids[kid["id"]] = { "switches" : [], "name" : kid["name"], "value_accrued" : 0 }
        
        for task in kid["tasks"]:
            self.create_switch(kid["id"], kid["name"], task)

    def create_switch(self, id, name, task):
        topic = hass_kid_entity["generic_switch"]
        topic = topic.replace("#", id)
        topic = topic.replace("?", task["id"])

        config = hass_kid_entity["generic_switch_config"].copy()
        config["unique_id"] = "{}_{}_switch".format(id,task["name"])
        config["name"] = task["name"]
        config["state_topic"] = config["state_topic"].replace("#", id)
        config["state_topic"] = config["state_topic"].replace("?", task["id"])

        device = kids_device.copy()
        device["name"] = device["name"].replace("#", name)
        config["device"] = device

        config["command_topic"] = config["command_topic"].replace("#", id)
        config["command_topic"] = config["command_topic"].replace("?", task["id"])

        self.mqtt.client.publish(config["state_topic"], "off")
        self.mqtt.client.publish(topic, json.dumps(config), retain=True)

        self.mqtt.client.subscribe(config["command_topic"])

        self.kids[id]["switches"].append({"id": task["id"], "topic": topic, "config": config})
