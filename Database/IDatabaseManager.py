from abc import ABC, abstractmethod


class IDatabaseManager(ABC):
    @abstractmethod
    def __init__(self, host, port, user_name, user_password, db_name):
        pass

    @abstractmethod
    def is_rental(self, idm):
        pass

    @abstractmethod
    def regist(self, idm, umbrella_id):
        pass

    @abstractmethod
    def __del__(self):
        pass
