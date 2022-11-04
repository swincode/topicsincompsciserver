
import serial
from MachineStatus import MachineStatus


class SerialController:

    def __init__(self, serial_port: str, machine_id: str = None):
        self.ser = serial.Serial(port=serial_port, baudrate=9600, timeout=2)
        self.machine_type = None
        self.machine_id = machine_id
        self.machine_state = MachineStatus.IDLE
        self.order = None
        self.num_tasks_completed = 0

    def __del__(self):
        self.ser.close()

    def get_machine_state(self) -> dict:
        return {"id": self.machine_id, "state": self.machine_state.value}

    def close_serial(self):
        self.ser.close()

    def open_serial(self):
        self.ser.open()

    def write(self, write_str: str):
        self.ser.write(bytes(write_str, "UTF-8"))

    def read(self):
        line = self.ser.readline()
        line = str(line).replace('b', '').replace("'", "")[0: -2]
        return line
