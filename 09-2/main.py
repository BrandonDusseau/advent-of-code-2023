import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

sequences = []
final_values = []

for raw_line in lines:
    line = raw_line.strip()
    if line == "":
        continue
    sequences.append([int(x) for x in line.split()])

for sequence in sequences:
    steps = [sequence]
    while len([x for x in steps[-1] if x != 0]) != 0:
        new_sequence = []
        working_sequence = steps[-1]
        for i in range(1, len(working_sequence)):
            new_sequence.append(working_sequence[i] - working_sequence[i - 1])
        steps.append(new_sequence)

    for i in range(len(steps) - 1, 0, -1):
        steps[i - 1][0:0] = [steps[i - 1][0] - steps[i][0]]

    final_values.append(steps[0][0])

print(sum(final_values))