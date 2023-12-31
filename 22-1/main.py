import os
from pprint import pprint

class Brick(object):
    def __init__(self, x1, y1, z1, x2, y2, z2, id):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.id = id
        self.placed_top_z = None
        self.supported_by = set()
        self.supports = set()

    def height(self):
        return self.z2 - self.z1 + 1

    def __repr__(self):
        return f"[Brick {self.id} | {self.x1},{self.y1},{self.z1}~{self.x2},{self.y2},{self.z2} | Top: {self.placed_top_z} | Supported by: [{','.join([str(x) for x in self.supported_by])}] | Supports: [{','.join([str(x) for x in self.supports])}]]"

def get_sort_key(brick):
    return brick.z1

def will_collide_x(brick1, brick2):
    # Minimums exceed maximums, no overlap
    if brick1.x1 > brick2.x2 or brick2.x1 > brick1.x2:
        return False

    # Maximums below minimums, no overlap
    if brick1.x2 < brick2.x1 or brick2.x2 < brick1.x1:
        return False

    # Minimum exceeds other brick's minimum. We already know it's below the second brick's maximum.
    if brick1.x1 >= brick2.x1 or brick2.x1 >= brick1.x1:
        return True

    # Maximum lower than other brick's maximum. We already know it's above the second brick's minimum.
    if brick1.x2 <= brick2.x2 or brick2.x2 <= brick1.x2:
        return True

def will_collide_y(brick1, brick2):
    # Minimums exceed maximums, no overlap
    if brick1.y1 > brick2.y2 or brick2.y1 > brick1.y2:
        return False

    # Maximums below minimums, no overlap
    if brick1.y2 < brick2.y1 or brick2.y2 < brick1.y1:
        return False

    # Minimum exceeds other brick's minimum. We already know it's below the second brick's maximum.
    if brick1.y1 >= brick2.y1 or brick2.y1 >= brick1.y1:
        return True

    # Maximum lower than other brick's maximum. We already know it's above the second brick's minimum.
    if brick1.y2 <= brick2.y2 or brick2.y2 <= brick1.y2:
        return True

def can_be_removed(bricks, brick):
    for supported_brick_id in brick.supports:
        supported_brick = bricks[supported_brick_id]
        if len(supported_brick.supported_by) == 1:
            return False
    return True

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

bricks = []
brick_id = 0
for raw_line in raw_lines:
    line = raw_line.strip()
    if line == "":
        continue
    dim1, dim2 = line.split("~")
    x1, y1, z1 = dim1.split(",")
    x2, y2, z2 = dim2.split(",")
    min_x = min(x1, x2)
    max_x = max(x1, x2)
    min_y = min(y1, y2)
    max_y = max(y1, y2)
    min_z = min(z1, z2)
    max_z = max(z1, z2)
    bricks.append(Brick(int(min_x), int(min_y), int(min_z), int(max_x), int(max_y), int(max_z), brick_id))
    brick_id += 1

bricks = sorted(bricks, key=get_sort_key)
for i in range(0, len(bricks)):
    bricks[i].id = i

placed_bricks = set()
for brick in bricks:
    print(f"Processing brick {brick.id} ({brick.__repr__()})")
    collided_bricks_at_max_z = set()
    top_of_tallest_collision = 0
    for placed_brick_id in placed_bricks:
        placed_brick = bricks[placed_brick_id]

        collision = will_collide_x(brick, placed_brick) and will_collide_y(brick, placed_brick)

        if collision and placed_brick.placed_top_z > top_of_tallest_collision:
            top_of_tallest_collision = placed_brick.placed_top_z
            collided_bricks_at_max_z = set([placed_brick_id])
        elif collision and placed_brick.placed_top_z == top_of_tallest_collision:
            collided_bricks_at_max_z.add(placed_brick_id)

        if collision:
            print(f"  Collided with brick {placed_brick.__repr__()}")

    print(f"  Placed brick {brick.id} at layer {top_of_tallest_collision + 1}")
    brick.placed_top_z = top_of_tallest_collision + brick.height()
    brick.supported_by = collided_bricks_at_max_z.copy()
    for collided_brick_id in collided_bricks_at_max_z:
        bricks[collided_brick_id].supports.add(brick.id)
    placed_bricks.add(brick.id)
    print()

pprint(bricks)

print(len([x for x in bricks if can_be_removed(bricks, x)]))