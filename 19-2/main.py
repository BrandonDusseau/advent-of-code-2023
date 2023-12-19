import os
import re
from pprint import pprint

class WorkflowStep(object):
    def __init__(self, property, operator, value, action):
        self.property = property
        self.operator = operator
        self.value = value
        self.action = action

    def __repr__(self):
        return f"[if {self.property} {self.operator} {self.value} then do {self.action}]"

class Workflow(object):
    def __init__(self, name, steps):
        self.name = name
        self.steps = steps

    def __repr__(self):
        return f"[workflow {self.name} with steps {', '.join([step.__repr__() for step in self.steps])}]"

def find_accepted_routes(workflows, workflow_name, ranges):
    if workflow_name == "R":
        return None
    elif workflow_name == "A":
        return [ranges]

    workflow = workflows[workflow_name]
    acceptable_ranges = []
    cur_ranges = ranges.copy()
    for step in workflow.steps:
        pass

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

lines = [line.strip() for line in raw_lines]

workflows = {}
for i in range(0, len(lines)):
    if lines[i] == "":
        break

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

print("Heck")