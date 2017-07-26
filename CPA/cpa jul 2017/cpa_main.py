from process_system import *
from utils import *

STEP_SIZE = 10
NUMBER_OF_STEPS = 1000
NUMBER_OF_SPECIES = 1

STARTING_POPULATION = 10000

BIRTH_RATE = 0.1
DEATH_RATE = 0.01

BIOME_COMPOUND_OBTENTION_RATE = 0.01

compound_registry = {}
process_registry = {}
organelle_registry = {}

class Compound:
    def __init__(self, name, initial_amount, is_useful, volume):
        self.name = name
        self.is_useful = is_useful
        self.initial_amount = initial_amount
        self.volume = volume
        compound_registry[name] = self
        Process("purge " + name, {name: 1}, {})
        print("Registered compound: " + name)

class Process:
    def __init__(self, name, inputs, outputs):
        self.name = name
        self.inputs = inputs.copy()
        self.outputs = outputs.copy()
        process_registry[name] = self
        print("Registered process: " + name)

class Organelle:
    def __init__(self, name, storage_space, processes, composition):
        self.name = name
        self.storage_space = storage_space
        self.processes = processes.copy()
        self.composition = composition.copy()
        organelle_registry[name] = self
        print("Registered organelle: " + name)

species_index = 0
class Species:
    def __init__(self, population, organelles):
        global species_index
        self.id = species_index
        species_index += 1
        self.population = population
        self.storage_space = 0
        self.composition = {}
        self.processes = {"aminoacid synthesis": 0.2} # that's what the nucleus does
        self.organelles = organelles.copy()

        for organelle_name, amount in organelles.items():
            organelle = organelle_registry[organelle_name]
            for i in range(amount):
                self.storage_space += organelle.storage_space
                self.composition = addDict(self.composition, organelle.composition)
                self.processes = addDict(self.processes, organelle.processes)

        self.processor = Processor(self.storage_space, compound_registry, process_registry, self.processes)

        print("Species created successfully")

    def decreasePopulation(self):
        change = int(self.population * DEATH_RATE)
        self.population -= change

    def increasePopulation(self):
        max_change = int(self.population * BIRTH_RATE)

        # Finding the limiting compound if any.
        for compound_name, amount in self.composition.items():
            max_change = min(max_change, int(self.processor.compound_data[compound_name].amount / amount))

        # Transforming the compounds into population.
        for compound_name, amount in self.composition.items():
            self.processor.compound_data[compound_name].amount -= max_change * amount

        self.population += max_change

class Biome:
    def __init__(self, initial_compounds, compound_change):
        self.compounds = initial_compounds
        self.compound_change = compound_change
        print("Biome created successfully")

    def step(self):
        self.compounds = addDict(self.compounds, self.compound_change)
        for compound_name, amount in self.compounds.items():
            if amount < 0:
                self.compounds[compound_name] = 0

    def addCompounds(self, compunds_to_add):
        self.compounds = addDict(self.compounds, compunds_to_add)

# Defining compounds
print("")
Compound("atp", 40, True, 1.0)
Compound("oxygen", 20, False, 1.0)
Compound("glucose", 10, False, 1.0)
Compound("co2", 10, False, 1.0)
Compound("ammonia", 0, False, 1.0)
Compound("aminoacids", 0, True, 1.0)

# Defining processes
print("")
Process("respiration", {"glucose": 1, "oxygen": 6}, {"atp": 36, "co2": 6})
Process("photosynthesis", {"co2": 6}, {"glucose": 1, "oxygen": 6})
Process("aminoacid synthesis", {"glucose": 1, "ammonia": 1}, {"atp": 1, "aminoacids": 1, "co2": 1})

# Defining organelles
print("")
Organelle("vacuole", 100, {}, {"glucose": 2, "aminoacids": 4})
Organelle("mitochondrion", 0, {"respiration": 0.07}, {"glucose": 2, "aminoacids": 4})
Organelle("chloroplast", 0, {"photosynthesis": 0.2}, {"glucose": 2, "aminoacids": 4})

print("")
patch = [Species(STARTING_POPULATION, {"vacuole": 2, "mitochondrion": 1}) for i in range(NUMBER_OF_SPECIES)]

print("")
biome = Biome({"oxygen": 30000, "co2": 75000, "ammonia": 4250, "glucose": 32500}, {"oxygen": 300, "co2": 750, "ammonia": 425, "glucose": 325})

for i in range(NUMBER_OF_STEPS):
    #print("")
    purged_compounds = {}
    for species in patch:
        for compound_name, compound_amount in biome.compounds.items():
            amount = compound_amount * BIOME_COMPOUND_OBTENTION_RATE
            species.processor.compound_data[compound_name].amount += amount
            biome.compounds[compound_name] -= amount

        species.processor.step(STEP_SIZE, species.population, process_registry, compound_registry)
        species.increasePopulation()
        species.decreasePopulation()
        purged_compounds = addDict(purged_compounds, species.processor.purgeCompounds(process_registry, compound_registry))
        species.processor.printCompounds()
        print("Storage space: " + str(species.processor.free_space))
        print("Population of " + str(species.id) + ": " + str(species.population))
        print("")
        biome.step()
    biome.addCompounds(purged_compounds)
