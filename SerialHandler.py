
import time
import serial.tools.list_ports
from SerialController import SerialController
from SoftwareDefinedMachineryController import SoftwareDefinedMachineryController


class SerialHandler:

    def __init__(self):
        self.devices = self.configure_serial_ports()

    def __del__(self):
        print("del")
        # if self.devices is not None:
        #     for d in self.devices:
        #         d["device"].pop()

    def configure_serial_ports(self) -> dict:
        data_struct = {"1": [], "2": [], "3": []}
        ports = serial.tools.list_ports.comports()

        print(f"ports: {ports}")

        for port in ports:

            print(str(port).split(" ")[0])
            new_device = SerialController(serial_port=str(str(port).split(" ")[0]))
            time.sleep(2)
            new_device.write("init")
            time.sleep(0.5)
            machine_type = new_device.read()
            new_device.machine_id = 1 if machine_type == "scanner" else 2
            new_device.machine_type = machine_type
            if len(data_struct["1"]) < 2:
                data_struct["1"].append(new_device)
            else:
                data_struct["2"].append(new_device)

        if data_struct["1"][0].machine_type == "mover":
            data_struct["1"].reverse()
        if data_struct["2"][0].machine_type == "mover":
            data_struct["2"].reverse()

        sdm1 = SoftwareDefinedMachineryController(machine_id=1)
        sdm1.machine_type = "scanner"
        sdm2 = SoftwareDefinedMachineryController(machine_id=2)
        sdm2.machine_type = "mover"

        data_struct["3"].append(sdm1)
        data_struct["3"].append(sdm2)

        return data_struct

    def serial_write(self, machine_id: str, message: str):
        self.devices[machine_id].write(message=message)

    def get_serial_read(self):
        result = {}
        for d in self.devices:
            result[d["machine_id"]] = d["device"].read()
        return result
