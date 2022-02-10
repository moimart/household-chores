from mqtt_client import MQTTClient
from gcalendar import GoogleCalendar
from timer import Timer
from timeit import default_timer as timer
from config import config
from kids import Kids

class Service:
    def __init__(self):
        self.timer = Timer(5, self)
        self.gc = GoogleCalendar()
        self.mqtt = MQTTClient()
        self.kids = Kids(self.mqtt)
        self.dt = 0

    def on_timer(self, timer, elapsed):
        self.kids.start()
        events = self.gc.get_events()
        self.mqtt.update_garbage(events)
        timer.time = config["update_interval"]
        timer.active = True
        timer.reset()

    def start(self):
        while True:
            t0 = timer()
            self.timer.step(self.dt)
            self.mqtt.loop()
            t1 = timer()

            self.dt = t1 - t0

def main():
    service = Service()
    service.start()

if __name__ == '__main__':
    main()