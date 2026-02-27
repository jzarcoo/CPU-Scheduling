from collections import deque
from Process import Process
from Scheduler import Scheduler

class MLQ(Scheduler):
    """
    Multilevel Queue (MLQ) scheduling algorithm implementation. 
    This scheduler divides processes into three queues based on their priority levels 
    and schedules them using round-robin within each queue. 
    
    - Processes are assigned to queues based on their priority, with the range of priorities divided into three equal parts.
    - Processes cannot move between queues once assigned, but they can be preempted by higher priority processes.

    Attributes:
        time_quantum (int): The time quantum for round-robin scheduling within each queue.
        priority_step (int): The step size for determining queue assignment based on priority.
        processes (list): List of processes to be scheduled, sorted by arrival time.
        timeline (list): A list representing the execution timeline of processes.
        time (int): The current time in the scheduling simulation.
        i (int): Index for tracking process arrivals.
        queues (list): A list of deques representing the three priority queues.
        current (Process): The currently executing process.
        current_queue (int): The index of the queue from which the current process was selected.
        quantum_counter (int): Counter for tracking the time spent on the current process for round-robin scheduling.
    """

    def __init__(self, time_quantum):
        """
        Initializes the MLQ scheduler with a specified time quantum.
        Args:
            time_quantum (int): The time quantum for round-robin scheduling within each queue.
        """
        self.time_quantum = time_quantum

    def _assign_queue(self, priority):
        """
        Determines the queue index for a process based on its priority.
        Args:            
            priority (int): The priority level of the process.
        Returns:            
            int: The index of the queue to which the process should be assigned.
        """
        if priority < self.priority_step:
            return 0
        elif priority < 2 * self.priority_step:
            return 1
        else:
            return 2
        
    def _process_arrivals_preemptive(self):
        """
        Processes new arrivals at the current time, assigning them to the appropriate queues based on their priority.

        If a new process has a higher priority than the currently executing process, 
        it preempts the current process and is added to the front of its respective queue.
        """
        while self.i < len(self.processes) and self.processes[self.i].arrival <= self.time:
            proc = self.processes[self.i]
            queue_index = self._assign_queue(proc.priority)
            self.queues[queue_index].append(proc)
            if self.current and proc.priority < self.current.priority:
                self.queues[self.current_queue].appendleft(self.current)
                self.current = None
            self.i += 1

    def _select_next_process(self):
        """
        Selects the next process to execute from the highest priority non-empty queue.
        """
        for idx in range(3):
            if self.queues[idx]:
                self.current = self.queues[idx].popleft()
                self.current_queue = idx
                self.quantum_counter = 0
                if self.current.start_time is None:
                    self.current.start_time = self.time
                break

    def _execute_current_process(self):
        """
        Executes the currently selected process for one time unit, updating the timeline and handling process completion or quantum expiration.
        """
        self.timeline.append(self.current)
        self.current.remaining -= 1
        self.quantum_counter += 1
        
        if self.current.remaining == 0:
            self.current.finish_time = self.time + 1
            self.current.calculate_metrics()
            self.current = None
        elif self.quantum_counter == self.time_quantum:
            self.queues[self.current_queue].append(self.current)
            self.current = None

    def run(self, processes):
        """
        Runs the MLQ scheduling algorithm on a list of processes.
        Args:
            processes (list): A list of Process objects to be scheduled.
        Returns:
            list: A timeline of process execution, where each entry is either a Process ID or "Idle".
        """
        priority_range = max(p.priority for p in processes) - min(p.priority for p in processes) + 1
        self.priority_step = max(1, priority_range // 3)  
        self.processes = sorted(processes, key=lambda p: p.arrival)
        self.timeline = []
        self.time = 0
        self.i = 0
        self.queues = [deque() for _ in range(3)]
        self.current = None
        self.current_queue = None
        self.quantum_counter = 0
        while self.i < len(self.processes) or any(self.queues) or self.current:
            self._process_arrivals_preemptive()
            if not self.current:
                self._select_next_process()
            if self.current:
                self._execute_current_process()
            else:
                self.timeline.append("Idle")
            self.time += 1
        return self.timeline