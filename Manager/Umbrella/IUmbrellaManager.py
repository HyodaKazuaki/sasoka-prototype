from abc import ABC, abstractmethod


class IUmbrellaManager(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def check_umbrella_change(self, umbrella_set):
        pass

    @abstractmethod
    def rent_one(self):
        pass

    def give_back_one(self):
        pass
