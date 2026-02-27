# CPU Scheduling

**Authors**: Julieta Flores y Antonio Zarco

**Course**: Operating Systems

## Overview

### 1. Multilevel Feedback Queue (MLFQ)

This scheduler divides processes into three queues based on their priority levels and schedules them using *Round-Robin* in the first two queues and *FC-FS* in the last queue.

- Processes can **move** between queues based on their behavior (e.g., if they use up their time quantum).
- **Aging** is implemented to prevent starvation of lower priority processes.
- Higher priority processes can **preempt** lower priority ones.

### 2. Multilevel Queue (MLQ)

This scheduler divides processes into three queues based on their priority levels and schedules them using *Round-Robin* within each queue.

- Processes **cannot move** between queues once assigned, but they can be **preempted** by higher priority processes.
- Quantum for queue $i$ is time_quantum $\cdot (2^i)$, meaning higher priority queues have shorter quantums.


## Installation


```shell
pip install -r requirements.txt
```

```shell
python TestScheduler.py < processes.txt
```

Visualize results (.csv) in jupyter notebook `metrics.ipynb`

## References
