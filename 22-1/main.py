import os

class Brick(object):
    def __init__(self, x1, y1, z1, x2, y2, z2, id):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.id = id
        self.supported_by = set()
        self.supports = set()

def can_be_removed(bricks, brick):
    for supported_brick_id in brick.supports:
        supported_brick = bricks[supported_brick_id]
        if len(supported_brick.supported_by) == 1:
            return False
    return True

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

def print_space(space, largest_z, largest_x, largest_y):
    for z in range(largest_z, -1, -1):
        print(f"Layer {z}")
        for x in range(0, largest_x + 1):
            print_row = []
            for y in range (0, largest_y + 1):
                if space[z][x][y] is None:
                    print_row.append("  ")
                else:
                    print_row.append(f"{space[z][x][y]:02}")
            print("|".join(print_row))
        print()

bricks = []
brick_id = 0
for raw_line in raw_lines:
    line = raw_line.strip()
    if line == "":
        continue
    dim1, dim2 = line.split("~")
    x1, y1, z1 = dim1.split(",")
    x2, y2, z2 = dim2.split(",")
    bricks.append(Brick(int(x1), int(y1), int(z1), int(x2), int(y2), int(z2), brick_id))
    brick_id += 1

x_space = 0
y_space = 0
z_space = 0
for brick in bricks:
    x_space += abs(brick.x1 - brick.x2) + 1
    y_space += abs(brick.y1 - brick.y2) + 1
    z_space += abs(brick.z1 - brick.z2) + 1

# Space is upside-down for math reasons.
space = []
tallest_occupied_z = 0
largest_occupied_x = 0
largest_occupied_y = 0
for z in range (0, z_space):
    space.append([])
    for x in range(0, x_space):
        space[z].append([])
        for y in range(0, y_space):
            space[z][x].append(None)

for brick in bricks:
    min_x = min(brick.x1, brick.x2)
    max_x = max(brick.x1, brick.x2)
    min_y = min(brick.y1, brick.y2)
    max_y = max(brick.y1, brick.y2)
    min_z = min(brick.z1, brick.z2)
    max_z = max(brick.z1, brick.z2)
    height = abs(brick.z1 - brick.z2) + 1

    check_z = tallest_occupied_z
    collision = False
    while collision is False:
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if space[check_z][x][y] is not None:
                    collision = True
                    # Mark the brick we collided with as load bearing.
                    brick.supported_by.add(space[check_z][x][y])
                    bricks[space[check_z][x][y]].supports.add(brick.id)

        # We hit the ground, so we can't drop any further
        if check_z < 0 and not collision:
            collision = True

        check_z -= 1

    # Place the brick
    start_z = check_z + 2
    for z in range(start_z, start_z + height):
        tallest_occupied_z = max(z, tallest_occupied_z)
        for x in range(min_x, max_x + 1):
            largest_occupied_x = max(x, largest_occupied_x)
            for y in range(min_y, max_y + 1):
                largest_occupied_y = max(y, largest_occupied_y)
                space[z][x][y] = brick.id

    # print_space(space, tallest_occupied_z, largest_occupied_x, largest_occupied_y)

print(len([x for x in bricks if can_be_removed(bricks, x)]))