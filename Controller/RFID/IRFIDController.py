from abc import ABC, abstractmethod


class IRFIDController(ABC):
    @abstractmethod
    def __init__(self, rfid_module_id):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def __del__(self):
        pass
