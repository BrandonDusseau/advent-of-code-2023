import os
import math
from pprint import pprint

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

seeds = {}
seed_soil_map = {}
soil_fertilizer_map = {}
fertilizer_water_map = {}
water_light_map = {}
light_temperature_map = {}
temperature_humidity_map = {}
humidity_location_map = {}
min_location = math.inf

viable_humidity_ranges = []
viable_temperature_ranges = []
viable_light_ranges = []
viable_water_ranges = []
viable_fertilizer_ranges = []
viable_soil_ranges = []
viable_seed_ranges = []

def parse_mapping(start_index, the_map):
    line_index < len(lines)
    index = start_index
    while index < len(lines) and lines[index].strip() != "":
        split_line = lines[index].strip().split()
        the_map[int(split_line[0])] = (int(split_line[0]), int(split_line[1]), int(split_line[2]))
        index += 1
    return index

def add_in_between_seed_ranges(the_map):
    sorted_ranges = sorted(the_map.values(), key=lambda x: x[0])
    new_ranges = []
    for i in range(0, len(sorted_ranges) - 1):
        current_range = sorted_ranges[i]
        current_range_max = current_range[0] + current_range[1]
        next_range = sorted_ranges[i+1]
        next_range_min = next_range[0]
        if next_range_min > current_range_max + 1:
            diff = next_range_min - current_range_max
            new_ranges.append((current_range[0] + current_range[1] + 1, diff))
    pprint(new_ranges)

    updated_map = {}
    for item in sorted_ranges:
        updated_map[item[0]] = item
    for item in new_ranges:
        updated_map[item[0]] = item
    return dict(sorted(updated_map.items()))

def add_in_between_ranges(the_map):
    sorted_ranges = sorted(the_map.values(), key=lambda x: x[1])
    new_ranges = []
    for i in range(0, len(sorted_ranges) - 1):
        current_range = sorted_ranges[i]
        current_range_max = current_range[1] + current_range[2]
        next_range = sorted_ranges[i+1]
        next_range_min = next_range[1]
        if next_range_min > current_range_max + 1:
            diff = next_range_min - current_range_max
            new_ranges.append((current_range[0] + current_range[2] + 1, current_range[1] + current_range[2] + 1, diff))

    first_range_min = sorted_ranges[0][1]
    first_range_dest = sorted_ranges[0][0]
    if first_range_min > 0:
        distance_from_zero = first_range_min
        new_ranges.append((first_range_dest - distance_from_zero, 0, distance_from_zero))
    pprint(new_ranges)

    updated_map = {}
    for item in sorted_ranges:
        updated_map[item[0]] = item
    for item in new_ranges:
        updated_map[item[0]] = item
    return dict(sorted(updated_map.items()))

def is_valid_seed(num):
    for key, seed in seeds.items():
        if key < num:
            continue
        if num >= seed[0] and num <= seed[0] + seed[1]:
            return True
    return False

def get_source(map, dest):
    for key, mapping in map.items():
        if key < dest:
            continue
        (map_dest, map_source, map_range) = mapping
        if dest >= map_dest and dest <= map_dest + map_range:
            return map_source + (dest - map_dest)
    return dest

def able_to_traverse(location):
    humid = get_source(humidity_location_map, location)
    temp = get_source(temperature_humidity_map, humid)
    light = get_source(light_temperature_map, temp)
    water = get_source(water_light_map, light)
    fertilizer = get_source(fertilizer_water_map, water)
    soil = get_source(soil_fertilizer_map, fertilizer)
    seed = get_source(seed_soil_map, soil)
    return is_valid_seed(seed)

def get_viable_ranges(min_target, max_target, the_map):
    ranges = []
    for key, mapping in the_map.items():
        if key < min_target:
            continue
        (map_dest, map_source, map_range) = mapping
        if map_dest >= min_target and map_dest + map_range <= max_target:
            ranges.append(mapping)
    return ranges

def get_max_source(the_map):
    max_source = 0
    for mapping in the_map:
        (map_dest, map_source, map_range) = mapping
        if map_source + map_range > max_source:
            max_source = map_source + map_range
    return max_source

def get_min_source(the_map):
    min_source = math.inf
    for mapping in the_map:
        (map_dest, map_source, map_range) = mapping
        if map_source < min_source:
            min_source = map_source
    return min_source

# Parse the input file.
line_index = 0
seed_data = lines[line_index].strip().split(":")[1].split()
for i in range(0, len(seed_data), 2):
    seeds[int(seed_data[i])] = (int(seed_data[i]), int(seed_data[i + 1]))
line_index += 3
line_index = parse_mapping(line_index, seed_soil_map) + 2
line_index = parse_mapping(line_index, soil_fertilizer_map) + 2
line_index = parse_mapping(line_index, fertilizer_water_map) + 2
line_index = parse_mapping(line_index, water_light_map) + 2
line_index = parse_mapping(line_index, light_temperature_map) + 2
line_index = parse_mapping(line_index, temperature_humidity_map) + 2
parse_mapping(line_index, humidity_location_map)

# Sort them for ease on my eyes.
seeds = add_in_between_seed_ranges(seeds)
seed_soil_map = add_in_between_ranges(seed_soil_map)
soil_fertilizer_map = add_in_between_ranges(soil_fertilizer_map)
fertilizer_water_map = add_in_between_ranges(fertilizer_water_map)
water_light_map = add_in_between_ranges(water_light_map)
light_temperature_map = add_in_between_ranges(light_temperature_map)
temperature_humidity_map = add_in_between_ranges(temperature_humidity_map)
humidity_location_map = add_in_between_ranges(humidity_location_map)

# Determine our absolute maximum possible location.
max_location_start = list(humidity_location_map.keys())[0]
max_location = max_location_start + humidity_location_map[max_location_start][2]

viable_humidity_ranges = get_viable_ranges(0, max_location, humidity_location_map)
print(f"Humidity ranges: {len(viable_humidity_ranges)}/{len(humidity_location_map)}")
viable_temperature_ranges = get_viable_ranges(get_min_source(viable_humidity_ranges), get_max_source(viable_humidity_ranges), temperature_humidity_map)
print(f"Temperature ranges: {len(viable_temperature_ranges)}/{len(temperature_humidity_map)}")
viable_light_ranges = get_viable_ranges(get_min_source(viable_temperature_ranges), get_max_source(viable_temperature_ranges), light_temperature_map)
print(f"Light ranges: {len(viable_light_ranges)}/{len(light_temperature_map)}")
viable_water_ranges = get_viable_ranges(get_min_source(viable_light_ranges), get_max_source(viable_light_ranges), water_light_map)
print(f"Water ranges: {len(viable_water_ranges)}/{len(water_light_map)}")
viable_fertilizer_ranges = get_viable_ranges(get_min_source(viable_water_ranges), get_max_source(viable_water_ranges), fertilizer_water_map)
print(f"Fertilizer ranges: {len(viable_fertilizer_ranges)}/{len(fertilizer_water_map)}")
viable_soil_ranges = get_viable_ranges(get_min_source(viable_fertilizer_ranges), get_max_source(viable_fertilizer_ranges), soil_fertilizer_map)
print(f"Soil ranges: {len(viable_soil_ranges)}/{len(soil_fertilizer_map)}")
viable_seed_ranges = get_viable_ranges(get_min_source(viable_soil_ranges), get_max_source(viable_soil_ranges), seed_soil_map)
print(f"Seed ranges: {len(viable_seed_ranges)}/{len(seed_soil_map)}")

pprint(viable_humidity_ranges[0])
pprint(viable_temperature_ranges[0])
pprint(viable_light_ranges[0])
pprint(viable_water_ranges[0])
pprint(viable_fertilizer_ranges[0])
pprint(viable_soil_ranges[0])
pprint(viable_seed_ranges[0])

exit()

# Do something of a binary search now.
current_location = max_location // 2
offset = 0
while current_location - offset != 0:
    if able_to_traverse(current_location - offset):
        min_location = current_location - offset
        current_location = min_location // 2
        print(f"Found new minimum at {min_location}, moving to {current_location}")
        offset = 0
        continue
    if offset != 0 and able_to_traverse(current_location + offset):
        min_location = current_location + offset
        current_location = min_location // 2
        print(f"Found new minimum at {min_location}, moving to {current_location}")
        offset = 0
        continue
    offset += 1

print(min_location)
