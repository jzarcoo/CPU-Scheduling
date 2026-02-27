import csv
from copy import deepcopy
from Process import Process
from MLFQ import MLFQ
from MLQ import MLQ

def read_processes():
    """
    Reads process information from standard input and returns a list of Process objects.
    """
    processes = []
    try:
        while True:
            line = input()
            if not line.strip():
                break
            pid, arrival, burst, priority = map(int, line.split())
            processes.append(Process(pid, arrival, burst, priority))
    except EOFError:
        pass
    return processes

def write_timeline(timeline, name):
    """
    Writes the timeline of process execution to a CSV file.

    Args:
        timeline (list): A list representing the execution timeline of processes, where each entry is either a Process ID or "Idle".
        name (str): The base name for the output CSV file.
    """
    with open(f"{name}_timeline.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Process"])
        for time, proc in enumerate(timeline):
            writer.writerow([time, proc])

def write_metrics(processes, name):
    """
    Writes the metrics of each process to a CSV file.

    Args:
        processes (list): A list of Process objects, each containing metrics such as arrival time, burst time, priority, start time, finish time, waiting time, turnaround time, and response time.
        name (str): The base name for the output CSV file.
    """
    with open(f"{name}_metrics.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Process ID", "Arrival", "Burst", "Priority", "Start Time", "Finish Time", "Waiting Time", "Turnaround Time", "Response Time"])
        for p in processes:
            writer.writerow([f"P{p.id}", p.arrival, p.burst, p.priority, p.start_time, p.finish_time, p.waiting_time, p.turnaround, p.response_time])

def write_summary(context_switches, name):
    """
    Writes summary statistics to a CSV file.

    Args:
        context_switches (int): Total number of context switches.
        name (str): The base name for the output CSV file.
    """
    with open(f"{name}_summary.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total Context Switches", context_switches])

def main():
    processes = read_processes()
    if processes == []:
        print("No processes given")
        return
    time_quantum = 8
    scheduler = MLQ(time_quantum)
    processes_copy = deepcopy(processes)
    timeline = scheduler.run(processes_copy)
    write_timeline(timeline, "mlq")
    write_metrics(processes_copy, "mlq")
    write_summary(scheduler.context_switches, "mlq")

    time_quantum_q1 = 8
    time_quantum_q2 = 16
    aging_threshold = 100
    processes_copy = deepcopy(processes)
    scheduler_mlfq = MLFQ(time_quantum_q1, time_quantum_q2, aging_threshold)
    timeline_mlfq = scheduler_mlfq.run(processes_copy)
    write_timeline(timeline_mlfq, "mlfq")
    write_metrics(processes_copy, "mlfq")
    write_summary(scheduler_mlfq.context_switches, "mlfq")

    print("All schedulers completed successfully. View results in metrics.ipynb")
if __name__ == "__main__":
    main()