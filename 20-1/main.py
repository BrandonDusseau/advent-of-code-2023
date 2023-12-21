import os

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

def push_button(pulse_queue, modules):
    high_pulses_sent = 0
    low_pulses_sent = 1

    pulse_queue.append(Pulse("button", "broadcaster", False))
    while len(pulse_queue) != 0:
        next_pulse = pulse_queue.pop(0)
        if next_pulse.to not in modules:
            continue
        outputs = modules[next_pulse.to].execute(next_pulse)
        for output in outputs:
            if output.state:
                high_pulses_sent += 1
            else:
                low_pulses_sent += 1
        pulse_queue += outputs

    return (high_pulses_sent, low_pulses_sent)

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

# Initialize the memory of conjunctions.
for module in modules.values():
    for dest_module in module.to:
        if dest_module not in modules:
            continue
        if modules[dest_module].category == "conjunction":
            conjunction_inputs[dest_module].append(module.name)
for module_name, inputs in conjunction_inputs.items():
    modules[module_name].initialize(inputs)

pulse_queue = []
iterations = 0
high = 0
low = 0
while iterations < 1000:
    (iter_high, iter_low) = push_button(pulse_queue, modules)
    high += iter_high
    low += iter_low
    iterations += 1
    if check_module_defaults(modules):
        break

multiplier = 1000 // iterations
high *= multiplier
low *= multiplier

more_iterations = 1000 % iterations
print(f"Need to run {more_iterations} more times to reach 1000.")
for i in range(0, more_iterations):
    (iter_high, iter_low) = push_button(pulse_queue, modules)
    high += iter_high
    low += iter_low
print(f"High pulses: {high}, low pulses: {low}")
print(high * low)
