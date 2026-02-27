import random

# Generate diverse process set with random arrivals
num_processes = 100
processes = []

for i in range(1, num_processes + 1):
    arrival = random.randint(0, 300)  
    burst = random.randint(1, 100)  
    priority = random.randint(1, 5) 
    processes.append(f"{i} {arrival} {burst} {priority}")

# Write to file
with open('processes_random.txt', 'w') as f:
    f.write('\n'.join(processes))
    f.write('\n') 

print(f"Generated {num_processes} diverse processes")
print("Arrival time range: 0-200 (random)")
print("Priority range: 1-5")
print("Burst time range: 1-100")
print("Saved to processes_random.txt")
