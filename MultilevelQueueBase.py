from abc import ABC, abstractmethod
from Scheduler import Scheduler
from collections import deque

class MultilevelQueueBase(Scheduler, ABC):
    """
    Abstract base class for multilevel queue schedulers.
    Provides common functionality for assigning processes to queues and selecting processes.
    Subclasses must implement _process_arrivals_preemptive, _execute_current_process, and run.
    Subclasses must set self.num_queues in their __init__ method.
    """

    def _assign_queue(self, priority):
        """
        Determines the queue index for a process based on its priority.
        The priority range (0 to max priority) is divided equally among queues.
        Lower priority values are assigned to higher priority queues (queue 0).
        
        Args:            
            priority (int): The priority level of the process.
        Returns:            
            int: The index of the queue to which the process should be assigned.
        """
        for i in range(self.num_queues - 1):
            if priority < (i + 1) * self.priority_step:
                return i
        return self.num_queues - 1

    def _select_next_process(self):
        """
        Selects the next process to execute from the highest priority non-empty queue.
        """
        for idx in range(self.num_queues):
            if self.queues[idx]:
                self.current = self.queues[idx].popleft()
                self.current_queue = idx
                self.quantum_counter = 0
                if self.current.start_time is None:
                    self.current.start_time = self.time
                break

    def _initialize_state(self, processes):
        """
        Initializes common scheduler state before running.
        Calculates priority_step by dividing the range from 0 to max priority
        equally among the number of queues.
        """
        max_priority = max(p.priority for p in processes)
        self.priority_step = max(1, (max_priority + 1) // self.num_queues)
        self.processes = sorted(processes, key=lambda p: p.arrival)
        self.timeline = []
        self.time = 0
        self.i = 0
        self.queues = [deque() for _ in range(self.num_queues)]
        self.current = None
        self.current_queue = -1
        self.quantum_counter = 0
        self.context_switches = 0

    @abstractmethod
    def _process_arrivals_preemptive(self):
        """
        Processes new arrivals at the current time.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def _execute_current_process(self):
        """
        Executes the currently selected process.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def run(self, processes):
        """
        Runs the scheduling algorithm.
        Must be implemented by subclasses.
        """
        pass
