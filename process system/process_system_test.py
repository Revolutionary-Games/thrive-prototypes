from process_system import *

STEP_SIZE = 10
NUMBER_OF_STEPS = 1000

compound_registry = {}

class Compound:
    def __init__(self, name, initial_amount, is_useful, volume):
        self.name = name
        self.is_useful = is_useful
        self.initial_amount = initial_amount
        self.volume = volume
        compound_registry[name] = self
        print("Registered compound: " + name)

process_registry = {}

class Process:
    def __init__(self, name, inputs, outputs):
        self.name = name
        self.inputs = inputs.copy()
        self.outputs = outputs.copy()
        process_registry[name] = self
        print("Registered process: " + name)

# Defining compounds
print("")
Compound("atp", 40, True, 1.0)
Compound("oxygen", 20, False, 1.0)
Compound("glucose", 10, False, 1.0)
Compound("co2", 0, False, 1.0)

# Defining processes
print("")
Process("respiration", {"glucose": 1, "oxygen": 6}, {"atp": 36, "co2": 6})

p = Processor(100, compound_registry, process_registry, {"respiration": 0.07})

for i in range(NUMBER_OF_STEPS):
    p.step(STEP_SIZE, process_registry, compound_registry)
    print("")
    p.printCompounds()
