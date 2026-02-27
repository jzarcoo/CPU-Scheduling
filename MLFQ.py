from collections import deque
from Process import Process
from Scheduler import Scheduler

class MLFQ(Scheduler):
    """
    Multilevel Feedback Queue (MLFQ) scheduling algorithm implementation. 
    This scheduler divides processes into three queues based on their priority levels 
    and schedules them using round-robin in the first two queues and FCFS in the last queue.
    
    - Processes can move between queues based on their behavior (e.g., if they use up their time quantum).
    - Aging is implemented to prevent starvation of lower priority processes.
    - Higher priority processes can preempt lower priority ones.

    Attributes:
        time_quantum_q1 (int): The time quantum for round-robin scheduling in queue 1.
        time_quantum_q2 (int): The time quantum for round-robin scheduling in queue 2.
        aging_threshold (int): The threshold time after which a process is aged up.
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
    
    def __init__(self, time_quantum_q1, time_quantum_q2, aging_threshold):
        """
        Initializes the MLFQ scheduler with a specified time quantum.
        Args:
            time_quantum_q1 (int): The time quantum for round-robin scheduling in queue 1.
            time_quantum_q2 (int): The time quantum for round-robin scheduling in queue 2.
            aging_threshold (int): The threshold time after which a process is aged up.
        """
        self.time_quantum_q1 = time_quantum_q1
        self.time_quantum_q2 = time_quantum_q2
        self.aging_threshold = aging_threshold

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
            self.waiting_since[proc.id] = self.time
            if self.current and queue_index < self.current_queue:
                self.queues[self.current_queue].appendleft(self.current)
                self.waiting_since[self.current.id] = self.time
                self.current = None
            self.i += 1

    def _process_aging(self):
        """
        Implements aging by promoting processes that have been waiting for a long time in lower priority queues to higher priority queues.
        """
        for idx in range(1, 3):
            for _ in range(len(self.queues[idx])):
                proc = self.queues[idx].popleft()
                if self.time - self.waiting_since.get(proc.id, proc.arrival) >= self.aging_threshold:
                    self.queues[idx - 1].append(proc)
                    self.waiting_since[proc.id] = self.time
                else:
                    self.queues[idx].append(proc)
            
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
        
        - If the process finishes execution, it is marked as completed and removed from the current slot.
        - If the process reaches its time quantum limit without finishing, it is demoted to a lower priority queue (if applicable) and the scheduler selects the next process to execute.
        """
        self.timeline.append(self.current)
        self.current.remaining -= 1
        self.quantum_counter += 1
        
        if self.current.remaining == 0:
            self.current.finish_time = self.time + 1
            self.current.calculate_metrics()
            self.waiting_since.pop(self.current.id, None)
            self.current = None
        elif (self.current_queue == 0 and self.quantum_counter == self.time_quantum_q1) or (self.current_queue == 1 and self.quantum_counter == self.time_quantum_q2):
            if self.current_queue < 2:
                self.queues[self.current_queue + 1].append(self.current)
            else:
                self.queues[self.current_queue].append(self.current)
            self.waiting_since[self.current.id] = self.time + 1
            self.current = None

    def run(self, processes):
        """
        Runs the MLFQ scheduling algorithm on the given list of processes.
        Args:
            processes (list): A list of Process objects to be scheduled.
        Returns:
            list: A timeline of process execution, where each entry is a Process ID or "Idle".
        """
        self.processes = sorted(processes, key=lambda p: p.arrival)
        self.priority_step = max(p.priority for p in self.processes) // 3 + 1
        self.timeline = []
        self.time = 0
        self.i = 0
        self.queues = [deque() for _ in range(3)]
        self.current = None
        self.current_queue = -1
        self.quantum_counter = 0
        self.waiting_since = {}
        
        while self.i < len(self.processes) or any(self.queues) or self.current:
            self._process_arrivals_preemptive()
            self._process_aging()
            if not self.current:
                self._select_next_process()
            if self.current:
                self._execute_current_process()
            else:
                self.timeline.append("Idle")
            self.time += 1
        return self.timeline