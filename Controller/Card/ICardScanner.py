from abc import ABC, abstractmethod


class ICardScanner(ABC):
    @abstractmethod
    def __init__(self, device_name, target_list):
        pass

    @abstractmethod
    def scan_no_block(self):
        pass

    @abstractmethod
    def scan_with_block(self):
        pass

    @abstractmethod
    def pay_deposit(self, tag):
        pass

    @abstractmethod
    def return_deposit(self, tag):
        pass

    @abstractmethod
    def __del__(self):
        pass
