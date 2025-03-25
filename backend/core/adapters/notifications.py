from abc import ABC, abstractmethod


class AbstractNotifications(ABC):
    @abstractmethod
    def send(self, destination, message):
        raise NotImplementedError
