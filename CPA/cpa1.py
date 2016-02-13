import random
import math
from copy import deepcopy

#prototype for the CPA system for Thrive
#list of compounds
compounds = ["Sunlight", "Sulfur", "Hydrogen Sulfide", "Water", "Oxygen", "Hydrogen",
			"Nitrogen", "Carbon", "Carbon Dioxide", "Glucose", "Pyruvate", "Protein",
			"ATP", "Amino Acids", "Fat", "Ammonia", "Agent"]

permeability = {"Sunlight" : 0, 
				"Sulfur" : 0.5, 
				"Hydrogen Sulfide" : 0.5, 
				"Water" : 0.5, 
				"Oxygen" : 0.5, 
				"Hydrogen" : 0.5,
				"Nitrogen" : 0.5, 
				"Carbon" : 0.2, 
				"Carbon Dioxide" : 0.5, 
				"Glucose" : 0.1, 
				"Pyruvate" : 0.1, 
				"Protein" : 0,
				"ATP" : 0, 
				"Amino Acids" : 0, 
				"Fat" : 0.1, 
				"Ammonia" : 0.5, 
				"Agent" : 0}

#processes class
class process:
	def __init__(self, name, inputs, outputs, rate = 1):
		self.name = name
		self.inputs = inputs
		self.outputs = outputs
		self.rate = rate

#all the processes
processes = {}

processes["Photosynthesis"] = process("Photosynthesis", 
						{"Carbon Dioxide" : 2, "Water" : 6, "Sunlight" : 1},
						{"Glucose" : 1, "Oxygen" : 6})

processes["ChemoSynthesis"] = process("ChemoSynthesis", 
						{"Hydrogen Sulfide" : 12, "Carbon Dioxide" : 6},
						{"Glucose" : 1, "Water" : 6, "Sulfur" : 12})

processes["Glycolysis"] = process("Glycolysis", 
						{"Glucose" : 1},
						{"Pyruvate" : 2, "Hydrogen" : 4, "ATP" : 10})

processes["Respiration"] = process("Respiration", 
						{"Pyruvate" : 2, "Oxygen" : 5},
						{"Carbon Dioxide" : 6, "Water" : 4, "ATP" : 10})

processes["Hydrogen Reduction"] = process("Hydrogen Reduction", 
						{"Hydrogen" : 4, "Oxygen" : 2},
						{"Water" : 2,})

processes["Fat Synthesis"] = process("Fat Synthesis", 
						{"Pyruvate" : 8, "Water" : 10, "ATP" : 10},
						{"Fat" : 2, "Oxygen" : 17})

processes["Fat Respiration"] = process("Fat Respiration", 
						{"Fat" : 2, "Oxygen" : 17},
						{"Pyruvate" : 8, "Water" : 10, "ATP" : 8})

processes["Amino Acid Synthesis"] = process("Amino Acid Synthesis", 
						{"Pyruvate" : 2, "Ammonia" : 3, "ATP" : 5},
						{"Amino Acids" : 3, "Hydrogen": 8})

processes["Amino Acid Catabolism"] = process("Amino Acid Catabolism", 
						{"Amino Acids" : 3, "Hydrogen": 8, "ATP" : 5},
						{"Pyruvate" : 2, "Ammonia" : 3})

processes["Protein Synthesis"] = process("Protein Synthesis", 
						{"Amino Acids" : 4, "ATP" : 20},
						{"Protein" : 1})

processes["Protein Catabolism"] = process("Protein Catabolism", 
						{"Protein" : 1, "ATP" : 20},
						{"Amino Acids" : 4})

processes["Agent Synthesis"] = process("Agent Synthesis", 
						{"Protein" : 2, "ATP" : 10},
						{"Agent" : 1})

processes["Agent Catabolism"] = process("Agent Catabolism", 
						{"Agent" : 1, "ATP" : 10},
						{"Amino Acids" : 8})

#organelles class
class organelle:
	def __init__(self, name, processes):
		self.name = name
		self.processes = processes
		self.storage = 0

#all the organelles		
organelles = {}

organelles["Nucleus"] = organelle("Nucleus", 
				[processes["Protein Synthesis"], 
				processes["Amino Acid Synthesis"],
				processes["Fat Synthesis"],
				processes["Hydrogen Reduction"]])

organelles["Cytoplasm"] = organelle("Cytoplasm", 
				[processes["Glycolysis"], 
				processes["Amino Acid Catabolism"],
				processes["Fat Respiration"]])
organelles["Cytoplasm"].storage = 20

organelles["Chloroplast"] = organelle("Chloroplast", 
				[processes["Photosynthesis"]])

organelles["Chemoplast"] = organelle("Chemoplast", 
				[processes["ChemoSynthesis"]])

organelles["Mitochondria"] = organelle("Mitochondria", 
				[processes["Respiration"]])

organelles["Agent Gland"] = organelle("Agent Gland", 
				[processes["Agent Synthesis"]])

organelles["Protein Enzymes"] = organelle("Protein Enzymes", 
				[processes["Protein Catabolism"]])

organelles["Vacuole"] = organelle("Vacuole", [])
organelles["Vacuole"].storage = 100

#bacteria class
class bacterium:
	def __init__(self, name, processes):
		self.name = name
		self.processes = []
		self.processes.append(processes)


#all the bacteria, they don't spend ATP to break down anything
bacteria = {}

bacteria["Agent"] = bacterium("Agent", processes["Agent Catabolism"])
bacteria["Agent"].processes[0].inputs["ATP"] = 0

bacteria["Protein"] = bacterium("Protein", processes["Protein Catabolism"])
bacteria["Protein"].processes[0].inputs["ATP"] = 0

bacteria["Amino"] = bacterium("Amino", processes["Amino Acid Catabolism"])
bacteria["Amino"].processes[0].inputs["ATP"] = 0

#species class
class species:
	def __init__(self, number, patch):
		self.population = 50
		self.surface_area = 50
		self.patch = patch
		self.number = number
		self.organelles = []
		self.organelles.append(organelles["Nucleus"])
		#add organelles to the species, make sure there is only 1 nucleus
		number_of_organelles = random.randint(lower_organelles_per_species, upper_organelles_per_species)
		while number_of_organelles > 0:
			choice = random.choice(organelles.keys())
			if choice != "Nucleus":
				self.organelles.append(organelles[str(choice)])
				number_of_organelles -= 1
		#setup the compounds bins
		self.compounds_free = {}
		self.compounds_free_concentration = {}
		self.compounds_locked = {}
		for compound in compounds:
			self.compounds_free[str(compound)] = 100
			self.compounds_locked[str(compound)] = 100
		#setup the cell wall, permeability 0 means no transport, 1 means total transport
		self.permeability = permeability

	#compute the concentrations of compounds in the cell
	def compute_concentrations(self):
		total_compounds = sum(self.compounds_free.values())
		if total_compounds == 0:
			total_compounds += 0.001
		for compound in self.compounds_free.keys():
			self.compounds_free_concentration[str(compound)] = (
				float(self.compounds_free.get(str(compound)))/total_compounds)

	#for each organelle, for each process that organelle can do, run it
	def run_organelles(self):
		self.compute_concentrations()
		for organelle in self.organelles:
			for process in organelle.processes:
				#calculate the process rate
				# rate = base process rate * sum_i concentration(input i) * sum_j concentration(output i) 
				inputs_rate = 1
				outputs_rate = 1
				for compounds in process.inputs.keys():
					inputs_rate *= self.compounds_free_concentration[str(compounds)]
				for compounds in process.outputs.keys():
					inputs_rate *= (1 - self.compounds_free_concentration[str(compounds)])
				rate = process.rate*inputs_rate*outputs_rate
				#check there are enough inputs
				will_run = True
				for compounds in process.inputs.keys():
					if rate*process.inputs[str(compounds)] >= self.compounds_free[str(compounds)]:
						will_run = False
				#run the process
				if will_run:
					for compounds in process.inputs.keys():
						self.compounds_free[str(compounds)] -= rate*process.inputs[str(compounds)]
					for compounds in process.outputs.keys():
						self.compounds_free[str(compounds)] += rate*process.outputs[str(compounds)]

	def absorb(self):
		#absorb compounds from the patch
		#compare concentrations and then move towards equilibrium of partial pressures
		for compounds in self.compounds_free.keys():
			concentration_difference = (self.compounds_free_concentration[str(compounds)] - 
				self.patch.compounds_concentration[str(compounds)])
			#if there are enough compounds then absorb some 
			amount_to_absorb = concentration_difference*self.permeability[str(compounds)]
			if (self.compounds_free[str(compounds)] - amount_to_absorb >= 0 and
				self.patch.compounds[str(compounds)] + amount_to_absorb >= 0):
				self.compounds_free[str(compounds)] -= amount_to_absorb
				self.patch.compounds[str(compounds)] += amount_to_absorb

#patch class
class patch:
	def __init__(self, number, sunlight = 100):
		self.number = number
		self.sunlight = sunlight
		#put some species in each patch
		self.species = []
		for i in range(no_species_per_patch):
			self.species.append(species(i, self))
		#put some bacteria in each patch
		self.bacteria = []
		for bacterion in bacteria:
			self.bacteria.append(bacteria[str(bacterion)])
		#set environmental compounds
		self.compounds = {}
		for compound in compounds:
			self.compounds[str(compound)] = 100
		self.compounds_concentration = {}

	def compute_concentrations(self):
		total_compounds = sum(self.compounds.values())
		if total_compounds == 0:
			total_compounds += 0.001
		for compound in self.compounds.keys():
			self.compounds_concentration[str(compound)] = (
				float(self.compounds.get(str(compound)))/total_compounds)

	def run_bacteria(self):
		self.compute_concentrations()
		for bacterion in self.bacteria:
			for process in bacterion.processes:
			#rate is always equal to 1
			#check there are enough compounds
				will_run = True
				for compounds in process.inputs.keys():
					if process.inputs[str(compounds)] >= self.compounds[str(compounds)]:
						will_run = False
				#run the process
				if will_run:
					for compounds in process.inputs.keys():
						self.compounds[str(compounds)] -= process.inputs[str(compounds)]
					for compounds in process.outputs.keys():
						self.compounds[str(compounds)] += process.outputs[str(compounds)]

#initialise
no_species_per_patch = 3
no_of_patches = 2
lower_organelles_per_species = 5
upper_organelles_per_species = 20


class ocean:
	def __init__(self, patches, species, run_time):
		#get number of species and patches
		global no_species_per_patch
		no_species_per_patch = species
		global no_of_patches
		no_of_patches = patches	
		#get how many timesteps to do
		self.run_time = run_time
		#make some patches
		self.patches = []
		for i in range(no_of_patches):
			self.patches.append(patch(i))
		self.data = []

	def run_world(self):
		#main loop
		run_time = self.run_time
		for i in range(run_time):
			this_data = []
			for patch in self.patches:
				patch.run_bacteria()
				for species in patch.species:
					species.compounds_free["Sunlight"] = patch.sunlight
					species.run_organelles()
					species.absorb()
				this_data.append(deepcopy(patch))
			self.data.append(this_data)
				
					

