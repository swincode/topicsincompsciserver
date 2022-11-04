
import paho.mqtt.client as mqtt
from Config import MQTTConfig


class MQTTHandler:

    def __init__(self, data=None):
        self.data = data
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(MQTTConfig.HOST)

    def __del__(self):
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, result):
        print("Connected with result: ", result)

    def on_message(self, client, userdata, msg):
        # print(msg.topic, msg.payload)
        self.data.add_data(msg.topic, msg.payload)

    def publish(self, topic: str, payload: str):
        self.client.publish(topic=topic, payload=payload)

    def subscribe(self, topic: str):
        self.client.subscribe(topic=topic)

    def update(self):
        self.client.loop()
