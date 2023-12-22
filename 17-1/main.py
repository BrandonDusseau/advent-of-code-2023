import math
import os
from pprint import pprint

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

class Block(object):
    def __init__(self, row, col, heat_loss):
        self.row = row
        self.col = col
        self.heat_loss = heat_loss
        self.neighbors = []

    def get_key(self):
        return (self.row, self.col)

    def __repr__(self):
        print_neighbors = [f"({row}, {col})" for row, col in self.neighbors]
        return f"L: ({self.row}, {self.col}), H: {self.heat_loss}, N: [{' '.join(print_neighbors)}]"

def dijkstra(blocks, start):
    q = []
    dist = {}
    prev = {}

    for v in blocks:
        dist[v] = math.inf
        prev[v] = None
        q.append(v)
    dist[start.get_key()] = 0

    while len(q) != 0:
        min_dist = math.inf
        u = None
        for test_vertex in q:
            if dist[test_vertex] < min_dist:
                u = test_vertex
                min_dist = dist[test_vertex]
        q.remove(u)

        for neighbor_key in blocks[u].neighbors:
            neighbor = blocks[neighbor_key]
            if neighbor_key not in q:
                continue
            alt = dist[u] + neighbor.heat_loss
            if alt < dist[neighbor_key]:
                dist[neighbor_key] = alt
                prev[neighbor_key] = u

    return (dist, prev)

def get_shortest_path(blocks, start, goal):
    (dist, prev) = dijkstra(blocks, start)

    sequence = []
    u = goal.get_key()
    if prev.get(u) is not None or u == start.get_key():
        while u is not None:
            sequence.insert(0, blocks[u])
            u = prev.get(u)

    return sequence

def get_direction(a, b):
    if b.row > a.row:
        return "down"
    if b.row < a.row:
        return "up"
    if b.col < a.col:
        return "left"
    if b.col > a.col:
        return "right"
    return None

def validate_path(path):
    directions = []
    for i in range(1, len(path)):
        directions.append(get_direction(path[i - 1], path[i]))
        if len(directions) >= 4 and directions[-4] == directions[-3] and directions[-3] == directions[-2] and directions[-2] == directions[-1]:
            pprint(directions)
            return False
    return True

def delete_neighbor_in_direction(block, direction):
    for neighbor_key in block.neighbors:
        neighbor = blocks[neighbor_key]
        if get_direction(block, neighbor) == direction:
            block.neighbors.remove(neighbor_key)
            neighbor.neighbors.remove(block.get_key())
            print(f"Deleted {direction} neighbor from block {block}")
            return (block.get_key(), neighbor_key)
    return None

def delete_reverse_neighbor(block, last_direction):
    direction_to_delete = None
    if last_direction == "left":
        direction_to_delete = "right"
    elif last_direction == "right":
        direction_to_delete = "left"
    elif last_direction == "up":
        direction_to_delete = "down"
    elif last_direction == "down":
        direction_to_delete = "up"
    return delete_neighbor_in_direction(block, direction_to_delete)

def restore_neighbors(pairs):
    for pair in pairs:
        if pair is None:
            continue
        blocks[pair[0]].neighbors.append(pair[1])
        blocks[pair[1]].neighbors.append(pair[0])

blocks = {}
num_rows = 0
num_cols = 0

for raw_line in raw_lines:
    line = raw_line.strip()
    if line == "":
        continue

    split_line = list(line)
    for col in range(0, len(split_line)):
        blocks[(num_rows, col)] = (Block(num_rows, col, int(split_line[col])))
    num_rows += 1
    num_cols = len(split_line)

for loc, block in blocks.items():
    if block.row > 0:
        block.neighbors.append((block.row - 1, block.col))
    if block.col > 0:
        block.neighbors.append((block.row, block.col - 1))
    if block.row < num_rows - 1:
        block.neighbors.append((block.row + 1, block.col))
    if block.col < num_cols - 1:
        block.neighbors.append((block.row, block.col + 1))

current_position = blocks[(0, 0)]
shortest_path = [current_position]
goal = blocks[(num_rows - 1, num_cols - 1)]
last_three_directions = []
while current_position != goal:
    deleted_neighbors = []

    # We can't go backwards.
    if len(last_three_directions) != 0:
        deleted_neighbors.append(delete_reverse_neighbor(current_position, last_three_directions[-1]))

    # If we've traveled the same direction three times in a row, we can't proceed in that direction again.
    if len(last_three_directions) == 3 and len(set(last_three_directions)) == 1:
        deleted_neighbors.append(delete_neighbor_in_direction(current_position, last_three_directions[-1]))

    # Get the shortest path from here.
    next_shortest_path = get_shortest_path(blocks, current_position, goal)
    next_position = next_shortest_path[1]
    shortest_path.append(next_position)

    if len(last_three_directions) == 3:
        last_three_directions.pop(0)
    last_three_directions.append(get_direction(current_position, next_position))
    print(f"Moving {last_three_directions[-1]}")
    print()

    # Put back the neighbors we removed.
    restore_neighbors(deleted_neighbors)

    current_position = next_position

pprint(shortest_path)
print(sum([x.heat_loss for x in shortest_path]) - shortest_path[0].heat_loss)