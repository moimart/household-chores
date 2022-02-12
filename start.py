from mqtt_client import MQTTClient
from gcalendar import GoogleCalendar
from timer import Timer
from timeit import default_timer as timer
from kids import Kids
import yaml

class Service:
    def __init__(self):
        with open("config.yaml","r") as config:
            config = yaml.safe_load(config)

        self.timer = Timer(5, self)
        
        self.gc = GoogleCalendar(config["types_of_garbage"],
                                 config["garbage_translations"])

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
            self.mqtt.loop()
            self.kids.step(self.dt)
            t1 = timer()

            self.dt = t1 - t0

def main():
    service = Service()
    service.start()

if __name__ == '__main__':
    main()