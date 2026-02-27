from abc import ABC, abstractmethod
from Process import Process

class Scheduler(ABC):
    """
    Abstract class representing a CPU scheduling algorithm. 
    """

    @abstractmethod
    def run(self, processes):
        """
        Run the scheduling algorithm on the given list of processes.
        """
        pass