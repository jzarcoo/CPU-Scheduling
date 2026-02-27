import random

# Generate diverse process set
num_processes = 100
processes = []

for i in range(1, num_processes + 1):
    arrival = (i - 1) * 2  # Staggered arrivals
    burst = random.randint(1, 100)  # Burst time 1-100
    priority = random.randint(1, 5)  # Priority 1-5
    processes.append(f"{i} {arrival} {burst} {priority}")

# Write to file
with open('processes_diverse.txt', 'w') as f:
    f.write('\n'.join(processes))
    f.write('\n') 

print(f"Generated {num_processes} diverse processes")
print("Priority range: 1-5")
print("Burst time range: 1-100")
print("Saved to processes_diverse.txt")
