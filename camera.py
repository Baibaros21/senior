from abc import ABC, abstractmethod


class Camera(ABC):

    @abstractmethod
    def __init__(self, location):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def record(self):
        pass

    @abstractmethod
    def stop(self):
        pass 

    def error(self):
        return self.name + " at the "+ self.location + " is not working"