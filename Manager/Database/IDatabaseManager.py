from abc import ABC, abstractmethod


class IDatabaseManager(ABC):
    @abstractmethod
    def __init__(self, host, port, user_name, user_password, db_name):
        pass

    @abstractmethod
    def is_rental_idm(self, idm):
        pass

    @abstractmethod
    def is_rental_umbrella_id(self, umbrella_id):
        pass

    @abstractmethod
    def is_rental_umbrella_with_idm(self, umbrella_id, idm):
        pass

    @abstractmethod
    def record_rental(self, idm, umbrella_id):
        pass

    @abstractmethod
    def record_return(self, idm, umbrella_id):
        pass

    @abstractmethod
    def __del__(self):
        pass
