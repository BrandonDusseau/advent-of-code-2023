import os
import re

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

spring_maps = []
counts = []

def is_valid(map, counts):
    flattened_map = "".join(map)
    blocks = re.findall(r"#+", flattened_map)

    if len(blocks) != len(counts):
        return False

    for index in range(0, len(blocks)):
        if len(blocks[index]) != counts[index]:
            return False

    return True

def try_fill(map, expected_counts, expected_fill_count, damaged_locations, filled_locations):
    if len(filled_locations) == expected_fill_count or len(damaged_locations) == 0:
        map_copy = map.copy()
        for loc in filled_locations:
            map_copy[loc] = "#"
        if is_valid(map_copy, expected_counts):
            return 1
        else:
            return 0

    valid_count = 0
    for dl_index in range(0, len(damaged_locations)):
        loc = damaged_locations[dl_index]
        filled_loc_copy = filled_locations.copy()
        filled_loc_copy.append(loc)
        valid_count += try_fill(map, expected_counts, expected_fill_count, damaged_locations[dl_index + 1:], filled_loc_copy)

    return valid_count

lines = []
for raw_line in raw_lines:
    line = raw_line.strip()
    if line == "":
        continue
    lines.append(line)

for i in range(0, len(lines)):
    split_line = lines[i].split(" ")
    spring_maps.append(list(split_line[0]))
    counts.append([int(x) for x in split_line[1].split(",")])

def get_damaged_locations(map):
    damaged_locations = []
    for loc in range(0, len(map)):
        if map[loc] == "?":
            damaged_locations.append(loc)
    return damaged_locations

def get_number_of_springs(map):
    current_springs = 0
    for loc in range(0, len(map)):
        if map[loc] == "#":
            current_springs += 1
    return current_springs

arrangement_counts = []
for i in range(0, len(spring_maps)):
    spring_map = spring_maps[i]
    spring_counts = counts[i]
    expected_springs = sum(spring_counts)
    current_springs = get_number_of_springs(spring_map)
    damaged_locations = get_damaged_locations(spring_map)
    need_to_fill = expected_springs - current_springs

    # First get the result of <map>
    normal_result = try_fill(spring_map, spring_counts, need_to_fill, damaged_locations, [])

    doubled_spring_map = spring_map + ["?"] + spring_map
    doubled_spring_counts = spring_counts + spring_counts
    doubled_expected_springs = sum(doubled_spring_counts)
    doubled_current_springs = get_number_of_springs(doubled_spring_map)
    doubled_damaged_locations = get_damaged_locations(doubled_spring_map)
    doubled_need_to_fill = doubled_expected_springs - doubled_current_springs

    # Then get the result of <map>?<map> and determine our magic number
    double_result = try_fill(doubled_spring_map, doubled_spring_counts, doubled_need_to_fill, doubled_damaged_locations, [])
    multiplier = double_result // normal_result

    arrangement_counts.append(normal_result * (multiplier ** 4))

    print(f"{((i+1)/len(spring_maps)) * 100}% complete")

print(sum(arrangement_counts))
