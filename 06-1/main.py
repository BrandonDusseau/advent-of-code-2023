import os
import math

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

times = [int(x) for x in lines[0].split(":")[1].split()]
distances = [int(x) for x in lines[1].split(":")[1].split()]
ways_to_win = []

for i in range(0, len(times)):
    ways_to_win_this_race = 0
    time_available = times[i]
    distance_needed = distances[i]
    for charge_time in range(1, time_available + 1):
        travel_time = time_available - charge_time
        distance_traveled = travel_time * charge_time
        if distance_traveled > distance_needed:
            ways_to_win_this_race += 1
    ways_to_win.append(ways_to_win_this_race)

print(math.prod(ways_to_win))