
class Process:
    """
    Represents a process in a scheduling algorithm. 

    Attributes:
        id (int): Unique identifier for the process.
        arrival (int): Time at which the process arrives in the system.
        burst (int): Total CPU time required by the process.
        priority (int): Priority level of the process (lower value means higher priority).
        remaining (int): Remaining CPU time for the process (initially equal to burst).
        start_time (int): Time at which the process starts execution (initially None).
        finish_time (int): Time at which the process finishes execution (initially None).
        waiting_time (int): Total waiting time of the process (initially 0).
        turnaround (int): Total turnaround time of the process (initially 0).
        response_time (int): Time from arrival to first execution (initially None).
        context_switches (int): Number of times the process was context switched (initially 0).
    """

    def __init__(self, id, arrival, burst, priority):
        """
        Initialize a new process with the given attributes.

        Args:
            id (int): Unique identifier for the process.
            arrival (int): Time at which the process arrives in the system.
            burst (int): Total CPU time required by the process.
            priority (int): Priority level of the process (lower value means higher priority).
        """
        self.id = id
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining = burst
        self.start_time = None
        self.finish_time = None
        self.waiting_time = 0
        self.turnaround = 0
        self.response_time = None

    def calculate_metrics(self):
        """
        Calculate and update the waiting time, turnaround time, and response time for the process.
        """
        self.turnaround = self.finish_time - self.arrival
        self.waiting_time = self.turnaround - self.burst
        self.response_time = self.start_time - self.arrival

    def __repr__(self):
        """
        Return a string representation of the process.
        Returns:
            str: A string in the format "P{id}" where {id} is the process's unique identifier.
        """
        return f"P{self.id}"