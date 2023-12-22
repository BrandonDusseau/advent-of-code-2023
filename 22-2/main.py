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

def get_fall_count_bfs(bricks, start):
    queue = []
    explored = set([start])
    queue.append(start)
    while len(queue) != 0:
        next = queue.pop(0)
        print(f"Exploring {next}")

        # Skip the brick if it still has something standing under it and won't be cleared
        # by further exploring the queue.
        skip_brick = False
        if next != start:
            for supported_by_brick_id in bricks[next].supported_by:
                if supported_by_brick_id not in explored and supported_by_brick_id not in queue:
                    print(f"Skipping brick {next}")
                    skip_brick = True

        if skip_brick:
            if next in explored:
                explored.remove(next)
            continue

        for supported_brick_id in bricks[next].supports:
            if supported_brick_id not in explored:
                explored.add(supported_brick_id)
                queue.append(supported_brick_id)

    pprint(explored)
    return len(explored) - 1

def get_fall_count(bricks, brick_id, memo, explored):
    print(f"Processing brick {brick_id}")
    explored.add(brick_id)

    if brick_id in memo:
        print(f"  Memo total from beyond {brick_id} is {memo[brick_id]}")
        return memo[brick_id]

    brick = bricks[brick_id]
    if len(brick.supports) == 0:
        print(f"  Brick {brick_id} does not support anything")
        memo[brick_id] = 0
        return 0

    total = 0
    for supported_brick_id in brick.supports:
        if supported_brick_id in explored:
            print(f"  Skipping {supported_brick_id} because it's already been explored")
            continue
        total += 1 + get_fall_count(bricks, supported_brick_id, memo, explored)

    memo[brick_id] = total
    print(f"  Total from beyond {brick_id} is {total}")
    return total

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

    brick.placed_top_z = top_of_tallest_collision + brick.height()
    brick.supported_by = collided_bricks_at_max_z.copy()
    for collided_brick_id in collided_bricks_at_max_z:
        bricks[collided_brick_id].supports.add(brick.id)
    placed_bricks.add(brick.id)

memo = {}
sum = 0
for i in range(0, len(bricks)):
    if not can_be_removed(bricks, bricks[i]):
        print(f"Block {i} will cause falling")
        sum += get_fall_count_bfs(bricks, i)

print(sum)