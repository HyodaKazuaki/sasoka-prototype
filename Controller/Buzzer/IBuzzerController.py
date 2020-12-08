from abc import ABC, abstractmethod


class IBuzzerController(ABC):
    @abstractmethod
    def __init__(self, pin):
        pass

    @abstractmethod
    def sound(self, frequency, sound_time):
        pass

    @abstractmethod
    def inpulse(self, frequency, sound_time):
        pass

    @abstractmethod
    def bell(self, frequency_1, frequency_2, sound_time_1, sound_time_2):
        pass

    @abstractmethod
    def alert(self, frequency, sound_time, num_repeat):
        pass

    @abstractmethod
    def __del__(self):
        pass
