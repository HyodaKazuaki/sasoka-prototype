from abc import ABC, abstractmethod


class IServoManager(ABC):
    @abstractmethod
    def __init__(self, umbrella_holder_list):
        pass

    @abstractmethod
    def lock(self):
        pass

    @abstractmethod
    def unlock_all(self):
        pass

    @abstractmethod
    def unlock(self, servo_id):
        pass

    @abstractmethod
    def __del__(self):
        pass
