from collections import deque
from MultilevelQueueBase import MultilevelQueueBase

class MLQ(MultilevelQueueBase):
    """
    Multilevel Queue (MLQ) scheduling algorithm implementation. 
    This scheduler divides processes into three queues based on their priority levels 
    and schedules them using round-robin within each queue. 
    
    - Processes are assigned to queues based on their priority, with the range of priorities divided into three equal parts.
    - Processes cannot move between queues once assigned, but they can be preempted by higher priority processes.
    - Quantum for queue i is time_quantum * (2^i), meaning higher priority queues have shorter quantums.

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
        num_queues (int): Number of queues (default: 3).
    """
    
    def __init__(self, time_quantum, num_queues=3):
        """
        Initializes the MLQ scheduler with a specified time quantum.
        Args:
            time_quantum (int): The time quantum for round-robin scheduling within each queue.
            num_queues (int): Number of queues (default: 3).
        """
        self.num_queues = num_queues
        self.time_quantum = time_quantum

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
        # Lower quantum for higher priority queues
        elif self.quantum_counter == self.time_quantum * (2 ** self.current_queue):
            self.queues[self.current_queue].append(self.current)
            self.current = None


    def run(self, processes):
        """
        Runs the MLQ scheduling algorithm on a list of processes.
        Args:
            processes (list): A list of Process objects to be scheduled.
        Returns:
            list: A timeline of process execution.
        """
        self._initialize_state(processes)
        prev_process = None
        
        while self.i < len(self.processes) or any(self.queues) or self.current:
            self._process_arrivals_preemptive()
            if not self.current:
                self._select_next_process()
            if self.current:
                if prev_process is not None and prev_process != self.current:
                    self.context_switches += 1
                self._execute_current_process()
                prev_process = self.current
            else:
                self.timeline.append("Idle")
                prev_process = None
            self.time += 1
        
        return self.timeline
