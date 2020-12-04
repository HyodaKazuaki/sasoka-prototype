from abc import ABC, abstractmethod

class IServoController(ABC):
    @abstractmethod
    def __init__(self, pin, unlock=2.5, lock=12.0, frequency=50, initialize_state=0):
        pass

    @abstractmethod
    def lock(self):
        pass

    @abstractmethod
    def unlock(self):
        pass
    
    @abstractmethod
    def __del__(self):
        pass