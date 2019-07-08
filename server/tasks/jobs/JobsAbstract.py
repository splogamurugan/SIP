from abc import ABC, abstractmethod

class JobsAbstract(ABC):

    @abstractmethod
    def retry_count(self):
        return 0

    @abstractmethod
    def handle(self, **kwargs):
        pass