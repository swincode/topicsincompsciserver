

from MachineStatus import MachineStatus


class SoftwareDefinedMachineryController:

    def __init__(self, machine_id: str = None):
        self.machine_type = None
        self.machine_id = machine_id
        self.machine_state = MachineStatus.IDLE
        self.read_val = None
        self.num_tasks_completed = 0

    def get_machine_state(self) -> dict:
        return {"id": self.machine_id, "state": self.machine_state.value}

    def write(self, write_str: str):
        print(f"SDM:{self.machine_state}, writing:{write_str}")
        self.read_val = "done" if self.machine_type == "scanner" else "complete"

    def read(self):
        return_val = self.read_val
        self.read_val = None
        return return_val
