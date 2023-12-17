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

    def __repr__(self):
        print_neighbors = [f"({x.row}, {x.col})" for x in self.neighbors]
        return f"L: ({self.row}, {self.col}), H: {self.heat_loss}, N: [{' '.join(print_neighbors)}]"

def dijkstra(blocks, start):
    q = set()

    dist = {}
    prev = {}

    for v in blocks:
        dist[v] = math.inf
        prev[v] = None
        q.add(v)
    dist[start] = 0

    while len(q) != 0:
        pprint(dist)
        min_dist = math.inf
        u = None
        for vertex in q:
            if dist[vertex] < min_dist:
                u = vertex
                min_dist = dist[vertex]
        q.remove(u)

        for neighbor in u.neighbors:
            if neighbor not in q:
                continue
            alt = dist[u] + neighbor.heat_loss
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = u

    return (dist, prev)

def get_shortest_path(blocks, start, goal):
    (dist, prev) = dijkstra(blocks.values(), start)

    sequence = []
    u = goal
    if prev.get(u) is not None or u == start:
        while u is not None:
            sequence[0:0] = [u]
            u = prev.get(u)

    return sequence


def yen(blocks, start, goal, goal_k):
    a = [get_shortest_path(blocks, start, goal)]
    b = []

    for k in range(1, goal_k):
        for i in range(0, len(a[k - 1]) - 2):
            spur_node = a[k - 1][i]
            root_path = a[k - 1][0:i + 1]

            removed_neighbors = []
            for path in a:
                if root_path == path[0:i + 1]:
                    removed_neighbors.append((path[i], path[i + 1]))
                    path[i].neighbors.remove(path[i + 1])

            removed_nodes = []
            for root_path_node in root_path:
                if root_path_node == spur_node:
                    continue
                removed_nodes.append(root_path_node)
                for removed_node_neighbor in root_path_node.neighbors:
                    removed_neighbors.append((removed_node_neighbor, root_path_node))
                    removed_node_neighbor.neighbors.remove(root_path_node)
                del blocks[(root_path_node.row, root_path_node.col)]

            spur_path = get_shortest_path(blocks, spur_node, goal)

            total_path = root_path + spur_path
            if total_path not in b:
                b.append(total_path)

            for removed_neighbor in removed_neighbors:
                if removed_neighbor[1] not in removed_neighbor[0].neighbors:
                    removed_neighbor[0].neighbors.append(removed_neighbor[1])

            for removed_node in removed_nodes:
                blocks[(removed_node.row, removed_node.col)] = removed_node

        if len(b) == 0:
            break

        min_cost = math.inf
        min_b_index = 0
        for i in range(0, len(b)):
            path_cost = sum([x.heat_loss for x in b[i]])
            if path_cost < min_cost:
                min_cost = path_cost
                min_b_index = i
        a[k] = b.pop(min_b_index)

    return a

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
            return False

    return True

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
        block.neighbors.append(blocks[(block.row - 1, block.col)])
    if block.col > 0:
        block.neighbors.append(blocks[(block.row, block.col - 1)])
    if block.row < num_rows - 1:
        block.neighbors.append(blocks[(block.row + 1, block.col)])
    if block.col < num_cols - 1:
        block.neighbors.append(blocks[(block.row, block.col + 1)])

calculated_paths = 100
path_is_valid = False
shortest_path = []
k = 0
shortest_paths = yen(blocks, blocks[(0, 0)], blocks[(num_rows - 1, num_cols - 1)], calculated_paths)
while not path_is_valid:
    print(f"Trying path {k}")
    shortest_path = shortest_paths[k]
    path_is_valid = validate_path(shortest_path)

    k += 1

    if k == calculated_paths - 1:
        calculated_paths *= 2
        print(f"Hydrating paths to {calculated_paths}")
        shortest_paths = yen(blocks, blocks[(0, 0)], blocks[(num_rows - 1, num_cols - 1)], calculated_paths)

pprint(shortest_path)
print(sum([x.heat_loss for x in shortest_path]) - shortest_path[0].heat_loss)