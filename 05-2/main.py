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

def parse_mapping(start_index, the_map):
    line_index < len(lines)
    index = start_index
    while index < len(lines) and lines[index].strip() != "":
        split_line = lines[index].strip().split()
        the_map[int(split_line[0])] = (int(split_line[0]), int(split_line[1]), int(split_line[2]))
        index += 1
    the_map = dict(sorted(the_map.items()))
    return index

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

# Determine our absolute maximum possible location.
max_location_start = list(humidity_location_map.keys())[0]
max_location = max_location_start + humidity_location_map[max_location_start][2]

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
