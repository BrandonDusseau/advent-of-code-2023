import math
import os
from pprint import pprint

class Pulse(object):
    def __init__(self, fr, to, state):
        self.fr = fr
        self.to = to
        self.state = state

    def __repr__(self):
        return f"[{self.state} pulse from {self.fr} to {self.to}]"

class Broadcaster(object):
    def __init__(self, to):
        self.name = "broadcaster"
        self.to = to
        self.category = "broadcaster"

    def execute(self, pulse):
        outputs = []
        for destination in self.to:
            outputs.append(Pulse("broadcaster", destination, pulse.state))
        return outputs

    def __repr__(self):
        return f"[broadcaster to {', '.join(self.to)}]"

class GenericModule(object):
    def __init__(self, name):
        self.to = []
        self.category = "generic"
        self.name = name

    def execute(self, pulse):
        return []

    def __repr__(self):
        return f"[generic module {self.name}]"

class FlipFlop(object):
    def __init__(self, name, to):
        self.name = name
        self.to = to
        self.state = False
        self.category = "flipflop"

    def execute(self, pulse):
        outputs = []

        if pulse.state:
            return outputs

        self.state = not self.state
        for destination in self.to:
            outputs.append(Pulse(self.name, destination, self.state))

        return outputs


    def __repr__(self):
        return f"[flipflop {self.name} to {', '.join(self.to)} with state {self.state}]"

class Conjunction(object):
    def __init__(self, name, to):
        self.name = name
        self.to = to
        self.memory = {}
        self.category = "conjunction"

    def initialize(self, inputs):
        for input in inputs:
            self.memory[input] = False

    def execute(self, pulse):
        outputs = []
        self.memory[pulse.fr] = pulse.state
        out_state = False in self.memory.values()
        for destination in self.to:
            outputs.append(Pulse(self.name, destination, out_state))

        return outputs

    def memory_strings(self):
        return [f"{key} => {value}" for key, value in self.memory.items()]

    def __repr__(self):
        return f"[conjunction {self.name} to {', '.join(self.to)} with memory ({', '.join(self.memory_strings())})]"

def dijkstra(modules, start):
    q = []
    dist = {}
    prev = {}

    for v in modules.keys():
        dist[v] = math.inf
        prev[v] = None
        q.append(v)
    dist[start] = 0

    while len(q) != 0:
        min_dist = math.inf
        u = None
        for vertex in q:
            if dist[vertex] < min_dist:
                u = vertex
                min_dist = dist[vertex]
        if u is None:
            return (None, None)
        q.remove(u)

        neighbors = []
        if u in modules:
            neighbors = modules[u].to
        for neighbor in neighbors:
            if neighbor not in q:
                continue
            alt = dist[u]
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = u

    return (dist, prev)

def get_shortest_path(modules):
    (dist, prev) = dijkstra(modules, "broadcaster")

    if dist is None:
        return None

    sequence = []
    u = "rx"
    if prev.get(u) is not None or u == "broadcaster":
        while u is not None:
            sequence[0:0] = [u]
            u = prev.get(u)

    return sequence

def push_button(pulse_queue, modules):
    low_pulses_sent_to_rx = 0

    pulse_queue.append(Pulse("button", "broadcaster", False))
    while len(pulse_queue) != 0:
        next_pulse = pulse_queue.pop(0)
        if next_pulse.to not in modules:
            continue
        outputs = modules[next_pulse.to].execute(next_pulse)
        for output in outputs:
            if not output.state and output.to == "rx":
                low_pulses_sent_to_rx += 1
        pulse_queue += outputs

    if low_pulses_sent_to_rx > 0:
        print(f"Lows sent to rx: {low_pulses_sent_to_rx}")
    return low_pulses_sent_to_rx

def check_module_defaults(modules):
    for module in modules.values():
        if module.category == "broadcaster":
            continue
        if module.category == "flipflop" and module.state:
            return False
        if module.category == "conjunction" and True in module.memory.values():
            return False
    return True

modules = {}
conjunction_inputs = {}

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

for raw_line in raw_lines:
    line = raw_line.strip()
    if line == "":
        continue

    (raw_module, raw_destination) = line.split(" -> ")
    destinations = raw_destination.split(", ")
    module_type = raw_module[0]
    module_name = raw_module[1:]

    if module_type == "b":
        modules["broadcaster"] = Broadcaster(destinations)
    elif module_type == "%":
        modules[module_name] = FlipFlop(module_name, destinations)
    elif module_type == "&":
        modules[module_name] = Conjunction(module_name, destinations)
        conjunction_inputs[module_name] = []
    else:
        print(f"Failed to parse input: {line}")
        exit(1)

# Initialize the memory of conjunctions and insert modules that go nowhere.
for module in modules.copy().values():
    for dest_module in module.to:
        if dest_module not in modules:
            modules[dest_module] = GenericModule(dest_module)
        if modules[dest_module].category == "conjunction":
            conjunction_inputs[dest_module].append(module.name)
for module_name, inputs in conjunction_inputs.items():
    modules[module_name].initialize(inputs)

shortest_path_to_rx = get_shortest_path(modules)
for mod_name in shortest_path_to_rx:
    pprint(modules[mod_name])
exit()

pulse_queue = []
iterations = 0
high = 0
low = 0
low_pulses_sent_to_rx = 0
while low_pulses_sent_to_rx != 1:
    low_pulses_sent_to_rx = push_button(pulse_queue, modules)
    iterations += 1

print(iterations)
