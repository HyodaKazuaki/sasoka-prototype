from abc import ABC, abstractmethod


class ICardScanner:
    @abstractmethod
    def __init__(self, device_name, target_list):
        pass

    @abstractmethod
    def scan(self):
        pass

    @abstractmethod
    def transact(self, idm):
        pass

    @abstractmethod
    def __del__(self):
        pass
