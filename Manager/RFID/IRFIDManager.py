from abc import ABC, abstractmethod


class IRFIDManager(ABC):
    @abstractmethod
    def __init__(self, umbrella_holder_list, num_try_to_get):
        pass

    @abstractmethod
    def get_all(self, number_rfid_reader):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def __del__(self):
        pass
