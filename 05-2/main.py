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
    return index

def get_destination(source, map):
    for mapping in map.values():
        (map_dest, map_source, map_range) = mapping
        if source in range(map_source, map_source + map_range):
            return map_dest + (source - map_source)
    return source

def prune_map(map, min_source, max_source):
    new_map = {}
    for key, value in map.items():
        (dest_start, src_start, range_len) = value
        if max_source < src_start:
            print(f"Source {src_start} is too high for maximum {max_source}, {key} is excluded")
            continue
        if min_source > src_start + range_len:
            print(f"Source {src_start} ({src_start + range_len}) is too low for minimum {min_source}, {key} is excluded")
            continue
        if max_source < src_start + range_len:
            new_range_len = max_source - src_start
            print(f"Source extends positively out of range for {max_source}, reducing range from {range_len} to {new_range_len} for {key}")
            range_len = new_range_len
        elif min_source > src_start:
            start_diff = min_source - src_start
            print(f"Source extends negatively out of range for {min_source}, adjusting ranges by {start_diff} for {key} (-> {dest_start + start_diff})")
            dest_start += start_diff
            src_start += start_diff
            range_len -= start_diff
        new_map[dest_start] = (dest_start, src_start, range_len)
    return new_map

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

pprint(seeds)
print()
# Sort the maps to process the lowest options first.
pprint(seed_soil_map)
seeds = dict(sorted(seeds.items()))
min_seed = min(seeds.keys())
max_seed_start = max(seeds.keys())
max_seed = max_seed_start + seeds[max_seed_start][1]
print(f"Minimum seed: {min_seed}")
print(f"Maximum seed: {max_seed}")
seed_soil_map = dict(sorted(prune_map(seed_soil_map, min_seed, max_seed).items()))
pprint(seed_soil_map)
print()
pprint(soil_fertilizer_map)
min_soil = min(min(seed_soil_map.keys()), min_seed)
max_soil_start = max(seed_soil_map.keys())
max_soil = max(max_soil_start + seed_soil_map[max_soil_start][2], max_seed)
print(f"Minimum soil: {min_soil}")
print(f"Maximum soil: {max_soil}")
soil_fertilizer_map = dict(sorted(prune_map(soil_fertilizer_map, min_soil, max_soil).items()))
pprint(soil_fertilizer_map)
print()
pprint(fertilizer_water_map)
min_fert = min(min(soil_fertilizer_map.keys()), min_seed)
max_fert_start = max(soil_fertilizer_map.keys())
max_fert = max(max_fert_start + soil_fertilizer_map[max_fert_start][2], max_seed)
print(f"Minimum fertilizer: {min_fert}")
print(f"Maximum fertilizer: {max_fert}")
fertilizer_water_map = dict(sorted(prune_map(fertilizer_water_map, min_fert, max_fert).items()))
pprint(fertilizer_water_map)
print()
pprint(water_light_map)
min_water = min(min(fertilizer_water_map.keys()), min_seed)
max_water_start = max(fertilizer_water_map.keys())
max_water = max(max_water_start + fertilizer_water_map[max_water_start][2], max_seed)
print(f"Minimum water: {min_water}")
print(f"Maximum water: {max_water}")
water_light_map = dict(sorted(prune_map(water_light_map, min_water, max_water).items()))
pprint(water_light_map)
print()
pprint(light_temperature_map)
min_light = min(min(water_light_map.keys()), min_seed)
max_light_start = max(water_light_map.keys())
max_light = max(max_light_start + water_light_map[max_light_start][2], max_seed)
print(f"Minimum light: {min_light}")
print(f"Maximum light: {max_light}")
light_temperature_map = dict(sorted(prune_map(light_temperature_map, min_light, max_light).items()))
pprint(light_temperature_map)
print()
pprint(temperature_humidity_map)
min_temp = min(min(light_temperature_map.keys()), min_seed)
max_temp_start = max(light_temperature_map.keys())
max_temp = max(max_temp_start + light_temperature_map[max_temp_start][2], max_seed)
print(f"Minimum temp: {min_temp}")
print(f"Maximum temp: {max_temp}")
temperature_humidity_map = dict(sorted(prune_map(temperature_humidity_map, min_temp, max_temp).items()))
pprint(temperature_humidity_map)
print()
pprint(humidity_location_map)
min_humid = min(min(temperature_humidity_map.keys()), min_seed)
max_humid_start = max(temperature_humidity_map.keys())
max_humid = max(max_humid_start + temperature_humidity_map[max_humid_start][2], max_seed)
print(f"Minimum humid: {min_humid}")
print(f"Maximum humid: {max_humid}")
humidity_location_map = dict(sorted(prune_map(humidity_location_map, min_humid, max_humid).items()))
pprint(humidity_location_map)

max_location_start = min(humidity_location_map.keys())
max_location = max_location_start + humidity_location_map[max_location_start][2]
print(f"Maximum location: {max_location}")

exit()

# Time to follow the maps.
for seed in seeds.values():
    for seed_num in range(seed[0], seed[0] + seed[1]):
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
