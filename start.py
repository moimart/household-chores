from mqtt_client import MQTTClient
from gcalendar import GoogleCalendar
from timer import Timer
from timeit import default_timer as timer
from kids import Kids
import yaml
import os
import json
from homeassistant_api import Client

class Service:
    def __init__(self):
        try:
            with open("chores_config.yaml","r") as config:
                config = yaml.safe_load(config)
        except Exception as e:
            with open("rename_to_config.yaml","r") as config:
                config = yaml.safe_load(config)

        translations = dict()

        self.timer = Timer(5, self)

        types_of_garbage = config["types_of_garbage"]
        translations = config["garbage_translations"]

        if "CONFIG_PATH" in os.environ:
            with open(os.environ['CONFIG_PATH'],mode="r") as options_file:
                config = json.load(options_file)

            types_of_garbage = config["types_of_garbage"]

            for item in config["garbage_translations"]:
                translations[item["id"]] = item["tr"]

        self.gc = GoogleCalendar(types_of_garbage, translations)

        if 'MQTT_HOST' in os.environ:
            self.mqtt = MQTTClient(os.environ['MQTT_USER'],
                                    os.environ['MQTT_PASSWORD'],
                                    os.environ['MQTT_HOST'],
                                    int(os.environ['MQTT_PORT']))
        else:
            self.mqtt = MQTTClient(config["mqtt"]["username"],
                                    config["mqtt"]["password"],
                                    config["mqtt"]["host"],
                                    config["mqtt"]["port"])

        self.kids = Kids(self.mqtt)
        self.dt = 0
        self.update_interval = config["update_interval"]

    def on_timer(self, timer, elapsed):
        events = self.gc.get_events()
        self.mqtt.update_garbage(events)
        timer.time = self.update_interval
        timer.active = True
        timer.reset()

    def start(self):
        self.kids.start()
        while True:
            t0 = timer()
            self.timer.step(self.dt)
            self.mqtt.step(self.dt)
            self.kids.step(self.dt)
            t1 = timer()

            self.dt = t1 - t0

def main():
    service = Service()
    service.start()

if __name__ == '__main__':
    main()