import os
from pprint import pprint

class HailStone(object):
    def __init__(self, px, py, pz, vx, vy, vz):
        self.px = px
        self.py = py
        self.pz = pz
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def __repr__(self):
        return f"[Hail stone ({self.px}, {self.py}, {self.pz}) with veolcity ({self.vx}, {self.vy}, {self.vz})]"

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

stones = []
for raw_line in raw_lines:
    line = raw_line.strip()
    if line == "":
        continue
    positions, velocities = line.split(" @ ")
    px, py, pz = positions.split(", ")
    vx, vy, vz = velocities.split(", ")
    stones.append(HailStone(int(px), int(py), int(pz), int(vx), int(vy), int(vz)))

pprint(stones)