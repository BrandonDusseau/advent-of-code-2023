import os
import re
from pprint import pprint

class Part(object):
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def __repr__(self):
        return f"(x={self.x}, m={self.m}, a={self.a}, s={self.s})"

class WorkflowStep(object):
    def __init__(self, property, operator, value, action):
        self.property = property
        self.operator = operator
        self.value = value
        self.action = action

    def get_property_value(self, part):
        if self.property == "x":
            return part.x
        if self.property == "m":
            return part.m
        if self.property == "a":
            return part.a

        return part.s

    def execute(self, part):
        if self.property is None:
            return self.action

        part_value = self.get_property_value(part)
        compare_value = self.value

        if self.operator == ">":
            return self.action if part_value > compare_value else None

        return self.action if part_value < compare_value else None

    def __repr__(self):
        return f"[if {self.property} {self.operator} {self.value} then do {self.action}]"

class Workflow(object):
    def __init__(self, name, steps):
        self.name = name
        self.steps = steps

    def execute(self, part):
        for step in self.steps:
            result = step.execute(part)
            if result is not None:
                return result

    def __repr__(self):
        return f"[workflow {self.name} with steps {', '.join([step.__repr__() for step in self.steps])}]"

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

lines = [line.strip() for line in raw_lines]

workflows = {}
parts = []
parsing_parts=False

for i in range(0, len(lines)):
    if lines[i] == "":
        parsing_parts = True
        continue

    if parsing_parts:
        part_match = re.match(r"\{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)\}", lines[i])
        if part_match is not None:
            parts.append(Part(int(part_match.group("x")), int(part_match.group("m")), int(part_match.group("a")), int(part_match.group("s"))))
        continue

    workflow_match = re.match(r"^(?P<name>[^\{}]+)\{(?P<steps>[^\}]+)\}", lines[i])
    if workflow_match is not None:
        name = workflow_match.group("name")
        raw_steps = workflow_match.group("steps").split(",")

        steps = []

        for raw_step in raw_steps:
            step_match = re.match(r"^(!?(?P<property>[xmas])(?P<operator>[\<\>])(?P<value>\d+):)?(?P<goto>[a-zA-Z]+)", raw_step)
            if step_match is None:
                print(f"Unable to parse step {raw_step}")
                continue

            property = step_match.group("property")
            operator = step_match.group("operator")
            value = int(step_match.group("value")) if step_match.group("value") is not None else None
            action = step_match.group("goto")
            steps.append(WorkflowStep(property, operator, value, action))

        workflows[name] = Workflow(name, steps)

accepted = []
rejected = []
for part in parts:
    cur_workflow = "in"
    while cur_workflow not in ["A", "R"]:
        cur_workflow = workflows[cur_workflow].execute(part)

    if cur_workflow == "A":
        accepted.append(part)
    else:
        rejected.append(part)

print("Accepted:")
pprint(accepted)
print()
print("Rejected:")
pprint(rejected)
print()
print(sum([p.x + p.m + p.a + p.s for p in accepted]))