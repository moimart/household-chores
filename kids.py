from devices import kids_device, hass_kid_entity, hass_kid_sensor
import yaml
import json
from timer import Timer
import pycron

class Kids:
    def __init__(self, mqtt):
        self.mqtt = mqtt
        self.mqtt.delegate = self
        self.kids = dict()
        self.timer = Timer(60, self)

    def on_timer(self, timer, elapsed):
        if pycron.is_now("0 0 * * *"):
            self.reset_switches()
        self.timer.reset()
        self.timer.active = True

    def start(self):
        with open("kids.yaml") as file:
            kidsconf = yaml.safe_load(file)

        if kidsconf is None:
            print("No kids found")
            return
        
        for kid in kidsconf["kids"]:
            self.create_kid(kid)

    def process_button(self, kid, swid, payload):
        payload = payload.decode("utf-8")

        for switch in kid["switches"]:
            if switch["id"] == swid:
                if payload == 'ON':
                    self.mqtt.client.publish(switch["config"]["state_topic"], "true")
                    kid["value_accrued"] += switch["value"];
                elif payload == 'OFF':
                    self.mqtt.client.publish(switch["config"]["state_topic"], "false")
                    kid["value_accrued"] -= switch["value"];
                else:
                    print("Unknown payload: {}".format(payload))
                print("Value accrued: {}".format(kid["value_accrued"]))
                self.mqtt.client.publish(kid["config"]["state_topic"], kid["value_accrued"], retain = True)
                return

    def step(self, dt):
        self.timer.step(dt)

    def reset_switches(self):
        if not bool(self.kids):
            return
        print("Resseting switches")
        for kid in self.kids.values():
            value = kid["value_accrued"]
            for switch in kid["switches"]:
                self.mqtt.client.publish(switch["config"]["state_topic"], "false")
                self.mqtt.client.publish(kid["config"]["state_topic"], value, retain = True)

    def on_message(self, topic, payload):
        if "command" in topic:
            self.process_button(self.kids[topic.split("/")[2]],topic.split("/")[3], payload)
        elif "state" in topic:
            print("{} State: {}".format(topic,payload))
            self.kids[topic.split("/")[3]]["value_accrued"] = float(payload.decode("utf-8"))
            print("V: {}".format(self.kids[topic.split("/")[3]]["value_accrued"]))

    def create_kid(self, kid):
        topic = hass_kid_sensor["generic_sensor"]
        topic = topic.replace("#", kid["id"])

        config = hass_kid_sensor["generic_sensor_config"].copy()
        config["name"] = kid["name"]
        config["unique_id"] = "kid_" + kid["id"]
        config["state_topic"] = config["state_topic"].replace("#", kid["id"])

        device = kids_device.copy()
        device["name"] = device["name"].replace("#", kid["name"])
        device["model"] = "{}-{}".format(device["model"],kid["id"])
        config["device"] = device
        config["device"]["identifiers"][0] = "{} {}".format(config["device"]["identifiers"][0],kid["name"])

        self.mqtt.client.publish(config["state_topic"], 0)
        self.mqtt.client.publish(topic, json.dumps(config), retain=True)
        self.mqtt.client.subscribe(config["state_topic"])

        self.kids[kid["id"]] = { "switches" : [], "name" : kid["name"], "value_accrued" : 0, "config" : config }
        
        for task in kid["tasks"]:
            self.create_switch(kid["id"], kid["name"], task)

    def create_switch(self, id, name, task):
        topic = hass_kid_entity["generic_switch"]
        topic = topic.replace("#", id)
        topic = topic.replace("?", task["id"])

        config = hass_kid_entity["generic_switch_config"].copy()
        config["unique_id"] = "{}_{}_switch".format(id,task["id"])
        config["object_id"] = "{}_{}_switch".format(id,task["id"])
        config["name"] = task["name"]
        config["state_topic"] = config["state_topic"].replace("#", id)
        config["state_topic"] = config["state_topic"].replace("?", task["id"])

        device = kids_device.copy()
        device["name"] = device["name"].replace("#", name)
        device["model"] = "{}-{}".format(device["model"],id)
        config["device"] = device

        config["command_topic"] = config["command_topic"].replace("#", id)
        config["command_topic"] = config["command_topic"].replace("?", task["id"])

        self.mqtt.client.publish(config["state_topic"], "off")
        self.mqtt.client.publish(topic, json.dumps(config), retain=True)

        self.mqtt.client.subscribe(config["command_topic"])

        self.kids[id]["switches"].append({"id": task["id"], "topic": topic, "config": config, "value": task["value"]})
