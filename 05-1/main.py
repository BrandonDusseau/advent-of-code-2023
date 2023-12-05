import os
import math

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

seeds = []
seed_soil_map = []
soil_fertilizer_map = []
fertilizer_water_map = []
water_light_map = []
light_temperature_map = []
temperature_humidity_map = []
humidity_location_map = []
min_location = math.inf

def parse_mapping(start_index, the_map):
    line_index < len(lines)
    index = start_index
    while index < len(lines) and lines[index].strip() != "":
        split_line = lines[index].strip().split()
        the_map.append((int(split_line[0]), int(split_line[1]), int(split_line[2])))
        index += 1
    return index

def get_destination(source, map):
    for mapping in map:
        (map_dest, map_source, map_range) = mapping
        if source in range(map_source, map_source + map_range):
            return map_dest + (source - map_source)
    return source

# Parse the input file.
line_index = 0
seeds = lines[line_index].strip().split(":")[1].split()
line_index += 3
line_index = parse_mapping(line_index, seed_soil_map) + 2
line_index = parse_mapping(line_index, soil_fertilizer_map) + 2
line_index = parse_mapping(line_index, fertilizer_water_map) + 2
line_index = parse_mapping(line_index, water_light_map) + 2
line_index = parse_mapping(line_index, light_temperature_map) + 2
line_index = parse_mapping(line_index, temperature_humidity_map) + 2
parse_mapping(line_index, humidity_location_map)

# Time to follow the maps.
for seed in seeds:
    seed_num = int(seed)
    soil_num = get_destination(seed_num, seed_soil_map)
    fertilizer_num = get_destination(soil_num, soil_fertilizer_map)
    water_num = get_destination(fertilizer_num, fertilizer_water_map)
    light_num = get_destination(water_num, water_light_map)
    temp_num = get_destination(light_num, light_temperature_map)
    humid_num = get_destination(temp_num, temperature_humidity_map)
    location_num = get_destination(humid_num, humidity_location_map)

    if location_num < min_location:
        min_location = location_num

print(min_location)
