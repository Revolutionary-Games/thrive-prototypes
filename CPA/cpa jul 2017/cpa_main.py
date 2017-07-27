from process_system import *
from utils import *

# The size of the steps used in the process system, which determine
# the maximum rate of the processes.
PROCESS_STEP_SIZE = 10

# The amount of process steps before a population step, aka how much
# time does a microbe have to produce compounds to reproduce.
NUMBER_OF_PROCESS_STEPS = 100

# The number of population steps in the simulation.
NUMBER_OF_POPULATION_STEPS = 1000

# The number of species a patch has.
NUMBER_OF_SPECIES = 10

# The starting population of each species.
STARTING_POPULATION = 10000

# The maximum percentage of the population that can reproduce in a
# population step (the actual amount can be lower if there aren't
# enough compounds to reproduce).
BIRTH_RATE = 0.1

# The percentage of the population that dies on each population step.
DEATH_RATE = 0.02

# The percentage of the biome's compounds that are released to
# the species.
BIOME_COMPOUND_OBTENTION_RATE = 0.01

# This dicts store the compounds, processes and organelles.
compound_registry = {}
process_registry = {}
organelle_registry = {}

class Compound:
    def __init__(self, name, initial_amount, is_useful, volume):
        self.name = name
        self.is_useful = is_useful
        self.initial_amount = initial_amount * STARTING_POPULATION
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
        self.composition = {"aminoacids": 4} # that's what the nucleus costs.
        self.processes = {"aminoacid synthesis": 0.5} # that's what the nucleus does.
        self.organelles = organelles.copy()

        for organelle_name, amount in organelles.items():
            organelle = organelle_registry[organelle_name]
            for i in range(amount):
                self.storage_space += organelle.storage_space
                self.composition = addDict(self.composition, organelle.composition)
                self.processes = addDict(self.processes, organelle.processes)

        self.processor = Processor(self.storage_space, compound_registry, process_registry, self.processes)

        print("Species created successfully")

    # Decreases the population in a population step.
    def decreasePopulation(self):
        change = int(self.population * DEATH_RATE)
        self.population -= change

    # Increases the population in a population step.
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
    # compound_change gets added on each turn to the biome compounds.
    def __init__(self, initial_compounds, compound_change):
        self.compounds = initial_compounds
        self.compound_change = compound_change
        print("Biome created successfully")

    # Updates the biome, adding the compound change to it.
    def step(self):
        self.compounds = addDict(self.compounds, self.compound_change)
        for compound_name, amount in self.compounds.items():
            if amount < 0:
                self.compounds[compound_name] = 0

    # Adds compounds to the biome (for example the ones purged by microbes).
    def addCompounds(self, compunds_to_add):
        self.compounds = addDict(self.compounds, compunds_to_add)

# Defining the compounds.
print("")
#environmental
Compound("sulfur", 10, False, 1.0)
Compound("hydrogensulphide", 10, False, 1.0)
Compound("oxygen", 20, False, 1.0)
Compound("co2", 10, False, 1.0)
Compound("ammonia", 0, False, 1.0)
Compound("phosphates", 0, False, 1.0)
#manufactured by microbes
Compound("atp", 40, False, 1.0)
Compound("glucose", 10, False, 1.0)
Compound("pyruvate", 10, False, 1.0)
Compound("aminoacids", 10, True, 1.0)
Compound("fat", 0, False, 1.0)
Compound("nucleotide", 0, False, 1.0)
Compound("protein", 0, True, 1.0)
Compound("agent", 0, True, 1.0)
Compound("DNA", 0, True, 1.0)


# Defining the processes.
print("")
Process("chemosynthesis", {"hydrogensulphide": 12, "co2": 6}, {"glucose": 1, "sulphur": 12})
Process("photosynthesis", {"co2": 6}, {"glucose": 1, "oxygen": 6})
Process("glycolysis", {"glucose": 1}, {"pyruvate": 2, "atp": 2})
Process("respiration", {"pyruvate": 1, "oxygen": 3}, {"atp": 18, "co2": 3})
Process("sulfur respiration", {"pyruvate": 1, "sulfur": 3}, {"atp": 8, "co2": 3, "hydrogensulphide" : 3})
Process("aminoacid synthesis", {"pyruvate": 1, "ammonia": 1, "atp": 3}, {"aminoacids": 1})
Process("aminoacid digestion", {"aminoacids": 1}, {"pyruvate": 1, "ammonia": 1})
Process("protein synthesis", {"aminoacids": 1, "atp": 4}, {"protein" : 1})
Process("protein digestion", {"protein" : 1}, {"aminoacids": 1})
Process("fat synthesis", {"pyruvate": 9, "atp": 56}, {"fat" : 1, "co2" : 9})
Process("fat digestion", {"fat" : 1, "co2" : 9}, {"pyruvate": 9, "atp": 45})
Process("nucleotide synthesis", {"glucose": 1, "phosphates": 1, "atp": 8, "aminoacids" : 2}, {"nucleotide" : 1})
Process("nucleotide digestion", {"nucleotide" : 1}, {"glucose": 1, "phosphates": 1, "aminoacids" : 2})
Process("agent synthesis", {"protein": 1, "atp" : 5}, {"agent" : 1})
Process("agent digestion", {"agent" : 1}, {"protein": 1})
Process("DNA synthesis", {"nucleotide": 1, "atp" : 5}, {"DNA" : 1})
Process("DNA digestion", {"DNA" : 1}, {"nucleotide": 1})


# Defining the organelles.
print("")
Organelle("vacuole", 100, {}, {"aminoacids": 4})
Organelle("mitochondrion", 0, {"respiration": 0.07}, {"aminoacids": 4})
Organelle("sulfur mitochondrion", 0, {"sulfur respiration": 0.07}, {"aminoacids": 4})
Organelle("chloroplast", 0, {"photosynthesis": 0.2}, {"aminoacids": 4})
Organelle("chemoplast", 0, {"chemosynthesis": 0.2}, {"aminoacids": 4})
Organelle("cytoplasm", 0, {"glycolysis": 0.2, 
                            "fat synthesis": 0.2, 
                            "fat digestion": 0.2,
                            "aminoacid synthesis": 0.2,
                            "aminoacid digestion": 0.2}, {"aminoacids": 4})
Organelle("agent gland", 0, {"agent synthesis": 0.2}, {"aminoacids": 4})
Organelle("nucleus", 0, {"nucleotide synthesis": 0.2, 
                            "DNA synthesis": 0.2, 
                            "protein synthesis": 0.2}, {"aminoacids": 4})
Organelle("lysosomes", 0, {"protein digestion": 0.2, 
                            "nucleotide digestion": 0.2, 
                            "DNA digestion": 0.2,
                            "agent digestion": 0.2}, {"aminoacids": 4})


# Creating the patch, aka the species list.
print("")
patch = [Species(STARTING_POPULATION, {"vacuole": 2, "mitochondrion": 1, "nucleus": 1, "cytoplasm":1, "lysosomes":1}) for i in range(NUMBER_OF_SPECIES)]

# Defining the biome.
print("")
biome = Biome({"oxygen": 30000, "co2": 75000, "ammonia": 80000, "glucose": 80000, "phosphates": 10000}, {"oxygen": 300, "co2": 750, "ammonia": 800, "glucose": 800, "phosphates": 100})

for i in range(NUMBER_OF_POPULATION_STEPS):
    #print("")
    purged_compounds = {}
    for j in range(NUMBER_OF_PROCESS_STEPS):
        for species in patch:
            for compound_name, compound_amount in biome.compounds.items():
                amount = compound_amount * BIOME_COMPOUND_OBTENTION_RATE
                species.processor.compound_data[compound_name].amount += amount
                biome.compounds[compound_name] -= amount

            species.processor.calculateStorageSpace(species.population)
            species.processor.step(PROCESS_STEP_SIZE, species.population, process_registry, compound_registry)
        
        biome.step()

    for species in patch:
        species.increasePopulation()
        species.decreasePopulation()
        purged_compounds = addDict(purged_compounds, species.processor.purgeCompounds(process_registry, compound_registry))
        #species.processor.printCompounds()
        print("Population of " + str(species.id) + ": " + str(species.population))
    print("")
    biome.addCompounds(purged_compounds)
