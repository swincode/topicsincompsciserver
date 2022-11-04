
class DataHandler:

    def __init__(self) -> object:
        self.data_objects = []

    def add_data(self, topic, msg):
        self.data_objects.append(Data(topic, msg))


class Data:

    def __init__(self, topic: str, msg: str):
        self.topic = topic
        self.msg = msg

    def get_data(self) -> dict:
        return {"topic": self.topic, "msg": self.msg}
