
import json
import threading
import time
from MQTTHandler import MQTTHandler
from DataHandler import DataHandler
from MachineStatus import MachineStatus
from SerialHandler import SerialHandler

data_handler = DataHandler()


def main():
    mqtt = MQTTHandler()
    serial_handler = SerialHandler()
    print(serial_handler.devices)
    t2 = threading.Thread(target=mqtt_sub)

    t2.start()
    for line in serial_handler.devices:
        init_payload = []
        for device in serial_handler.devices[line]:
            init_payload.append(device.get_machine_state())

        mqtt_pub(mqtt, f"line/{line}", json.dumps({"id": int(line[-1]), "machines": init_payload}))

    try:
        while True:
            '''
            recv mqtt msg to turn a specific machine on, then once completed, return completed status
            '''
            time.sleep(0.1)
            if data_handler.data_objects is not []:
                for msg in data_handler.data_objects:
                    topic = msg.topic.split("/")
                    if len(topic) == 7 and serial_handler.devices[topic[1]][int(topic[3]) - 1].machine_state.value != "BROKEN":
                        serial_handler.devices[topic[1]][int(topic[3]) - 1].order = topic[5]
                        serial_handler.devices[topic[1]][int(topic[3]) - 1].machine_state = MachineStatus.WORKING
                        mqtt_pub(mqtt, f"line/{topic[1]}/machine/{topic[3]}/update",
                                 json.dumps(
                                     {"id": f"{int(topic[3])}",
                                      "state": f"{serial_handler.devices[topic[1]][int(topic[3]) - 1].machine_state.value}",
                                      "orderId": f"{serial_handler.devices[topic[1]][int(topic[3]) - 1].order}"})
                                 )
                        if topic[3] == "1":
                            serial_handler.devices[topic[1]][int(topic[3]) - 1].write("scan")
                        else:
                            serial_handler.devices[topic[1]][int(topic[3]) - 1].write("move_product")
                data_handler.data_objects = []

            for line in serial_handler.devices:
                for device in serial_handler.devices[line]:
                    ser_read_val = device.read()
                    if ser_read_val == "done" or ser_read_val == "complete":
                        if line == '1' and device.machine_id == 2 and device.num_tasks_completed >= 2:
                            device.machine_state = MachineStatus.BROKEN
                        else:
                            device.num_tasks_completed += 1
                            device.machine_state = MachineStatus.IDLE
                        mqtt_pub(mqtt, f"line/{line}/machine/{device.machine_id}/update",
                                 json.dumps({"id": f"{device.machine_id}", "state": device.machine_state.value,
                                             "orderId": f"{serial_handler.devices[topic[1]][int(topic[3]) - 1].order}"}))
                        time.sleep(0.1)
                        if device.machine_state.value != "BROKEN":
                            mqtt_pub(mqtt, f"line/{line}/machine/{device.machine_id}/order/{device.order}/complete",
                                     '{"order_complete": "True"}')

    except KeyboardInterrupt:
        print("Shutting down")
        t2.join(timeout=1.0)


def mqtt_sub():
    mqtt = MQTTHandler(data=data_handler)
    mqtt.subscribe(topic="line/+/machine/+/update")
    mqtt.subscribe(topic="line/+/machine/+/order/+/assign")
    while True:
        mqtt.update()


def mqtt_pub(mqtt: MQTTHandler, topic: str, payload: str):
    print(f"pub_(topic: {topic}, payload: {str(payload)})")
    mqtt.publish(topic=topic, payload=str(payload))


if __name__ == '__main__':
    main()
