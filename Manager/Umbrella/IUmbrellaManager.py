from abc import ABC, abstractmethod


class IUmbrellaManager(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def lock_all(self):
        pass

    @abstractmethod
    def lock_least_umbrellas(self):
        pass

    @abstractmethod
    def unlock_all(self):
        pass

    @abstractmethod
    def update_all_umbrella_id(self):
        pass

    @abstractmethod
    def rent_one(self):
        pass

    @abstractmethod
    def check_umbrella_was_returned(self):
        pass

    @abstractmethod
    def unlock_umbrella_for_failsafe(self, umbrella_holder):
        pass
