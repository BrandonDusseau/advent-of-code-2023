import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

time_available = int("".join(lines[0].split(":")[1].split()))
distance_needed = int("".join(lines[1].split(":")[1].split()))

ways_to_win_this_race = 0
for charge_time in range(1, time_available + 1):
    travel_time = time_available - charge_time
    distance_traveled = travel_time * charge_time
    if distance_traveled > distance_needed:
        ways_to_win_this_race += 1

print(ways_to_win_this_race)