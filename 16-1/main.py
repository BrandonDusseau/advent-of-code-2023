import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

class Beam(object):
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction

    def to_string(self):
        return f"{self.row}-{self.col}-{self.direction}"

    def __repr__(self):
        print(f"Beam end at ({self.row}, {self.col}) heading {self.dir}")

grid = []
splitters = ["|", "-"]
mirrors = ["/", "\\"]

beams = [Beam(0, -1, "right")]
seen_beam_states = set()
energized_tiles = set()

def print_energized():
    for row in range(0, len(grid)):
        print_row = []
        for col in range(0, len(grid[0])):
            if (row, col) in energized_tiles:
                print_row.append("#")
            else:
                print_row.append(".")
        print("".join(print_row))
    print()

def print_grid_state():
    print_grid = []
    for row in range(0, len(grid)):
        print_row = []
        for col in range(0, len(grid[0])):
            print_row.append(grid[row][col])
        print_grid.append(print_row)

    for beam in beams:
        print_grid[beam.row][beam.col] = "#"

    for row in print_grid:
        print("".join(row))

    print()

def position_valid(row, col):
    return row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0])

def split_beam(row, col, beam):
    beams.remove(beam)
    if grid[row][col] == "|":
        if position_valid(row - 1, col):
            beams.append(Beam(row, col, "up"))
        if position_valid(row + 1, col):
            beams.append(Beam(row, col, "down"))

    if grid[row][col] == "-":
        if position_valid(row, col - 1):
            beams.append(Beam(row, col, "left"))
        if position_valid(row, col + 1):
            beams.append(Beam(row, col, "right"))

def reflect_beam(row, col, beam):
    mirror = grid[row][col]

    if mirror == "/":
        if beam.direction == "up":
            beam.direction = "right"
        elif beam.direction == "down":
            beam.direction = "left"
        elif beam.direction == "left":
            beam.direction = "down"
        else:
            beam.direction = "up"

    if mirror == "\\":
        if beam.direction == "up":
            beam.direction = "left"
        elif beam.direction == "down":
            beam.direction = "right"
        elif beam.direction == "left":
            beam.direction = "up"
        else:
            beam.direction = "down"

def move_next(beam):
    if beam.direction == "right" and position_valid(beam.row, beam.col + 1):
        next_pos = (beam.row, beam.col + 1)
    elif beam.direction == "left" and position_valid(beam.row, beam.col - 1):
        next_pos = (beam.row, beam.col - 1)
    elif beam.direction == "up" and position_valid(beam.row - 1, beam.col):
        next_pos = (beam.row - 1, beam.col)
    elif beam.direction == "down" and position_valid(beam.row + 1, beam.col):
        next_pos = (beam.row + 1, beam.col)
    else:
        beams.remove(beam)
        return

    energized_tiles.add(next_pos)
    next_tile = grid[next_pos[0]][next_pos[1]]

    if next_tile in ["/", "\\"]:
        reflect_beam(next_pos[0], next_pos[1], beam)
    elif (next_tile == "-" and beam.direction in ["up", "down"]) or (next_tile == "|" and beam.direction in ["left", "right"]):
        split_beam(next_pos[0], next_pos[1], beam)

    beam.row = next_pos[0]
    beam.col = next_pos[1]

for raw_line in raw_lines:
    line = raw_line.strip()
    if line == "":
        continue
    grid.append(list(line))

print_grid_state()
while len(beams) != 0:
    for beam in beams.copy():
        # Remove the beam if it's entering a loop.
        beam_string = beam.to_string()
        if beam_string in seen_beam_states:
            beams.remove(beam)
            continue

        seen_beam_states.add(beam_string)
        move_next(beam)
    print_grid_state()

print_energized()
print(len(energized_tiles))