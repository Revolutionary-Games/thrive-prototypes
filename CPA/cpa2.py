import random
import math
from copy import deepcopy

#prototype for the CPA system for Thrive
#list of compounds
compounds = ["Sunlight", "Sulfur", "Hydrogen Sulfide", "Water", "Oxygen", "Hydrogen",
			"Nitrogen", "Carbon", "Carbon Dioxide", "Glucose", "Pyruvate", "Protein",
			"ATP", "Amino Acids", "Fat", "Ammonia", "Agent"]

permeability = {"Sunlight" : 1, 
				"Sulfur" : 1, 
				"Hydrogen Sulfide" : 1, 
				"Water" : 1, 
				"Oxygen" : 1, 
				"Hydrogen" : 1,
				"Nitrogen" : 1, 
				"Carbon" : 1, 
				"Carbon Dioxide" : 1, 
				"Glucose" : 1, 
				"Pyruvate" : 1, 
				"Protein" : 1,
				"ATP" : 1, 
				"Amino Acids" : 1, 
				"Fat" : 1, 
				"Ammonia" : 1, 
				"Agent" : 1}

optimals = {"Sunlight" : 100, 
				"Sulfur" : 0, 
				"Hydrogen Sulfide" : 100, 
				"Water" : 100, 
				"Oxygen" : 100, 
				"Hydrogen" : 0,
				"Nitrogen" : 100, 
				"Carbon" : 0, 
				"Carbon Dioxide" : 100, 
				"Glucose" : 0, 
				"Pyruvate" : 0, 
				"Protein" : 0,
				"ATP" : 0, 
				"Amino Acids" : 0, 
				"Fat" : 0, 
				"Ammonia" : 100, 
				"Agent" : 0}

#processes class
class process:
	def __init__(self, name, inputs, outputs, rate = 1000):
		self.name = name
		#what compounds the process uses
		self.inputs = inputs
		#what compounds the process outputs
		self.outputs = outputs
		#speed of the process
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
	def __init__(self, name, processes, made_of):
		self.name = name
		#what processes the organelle can do
		self.processes = processes
		self.storage = 0
		#what the organelle is made of 
		self.made_of = made_of

#all the organelles		
organelles = {}

organelles["Nucleus"] = organelle("Nucleus", 
				[processes["Protein Synthesis"], 
				processes["Amino Acid Synthesis"],
				processes["Fat Synthesis"],
				processes["Hydrogen Reduction"]],
				{"Protein" : 2, "Fat" : 1})

organelles["Cytoplasm"] = organelle("Cytoplasm", 
				[processes["Glycolysis"], 
				processes["Amino Acid Catabolism"],
				processes["Fat Respiration"]],
				{"Protein" : 2, "Fat" : 1})
organelles["Cytoplasm"].storage = 20

organelles["Chloroplast"] = organelle("Chloroplast", 
				[processes["Photosynthesis"]],
				{"Protein" : 2, "Fat" : 1})

organelles["Chemoplast"] = organelle("Chemoplast", 
				[processes["ChemoSynthesis"]],
				{"Protein" : 2, "Fat" : 1})

organelles["Mitochondria"] = organelle("Mitochondria", 
				[processes["Respiration"]],
				{"Protein" : 2, "Fat" : 1})

organelles["Agent Gland"] = organelle("Agent Gland", 
				[processes["Agent Synthesis"]],
				{"Protein" : 2, "Fat" : 1})

organelles["Protein Enzymes"] = organelle("Protein Enzymes", 
				[processes["Protein Catabolism"]],
				{"Protein" : 2, "Fat" : 1})

organelles["Vacuole"] = organelle("Vacuole", [], {"Protein" : 2, "Fat" : 1})
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

#create a step function
#return positive if below low, negative if above high
def step_function(value, threshold, high_threshold, vent_threshold):
	if value >= high_threshold:
		return -float(value - high_threshold)/(vent_threshold - high_threshold)
	elif value >= threshold:
		return 0
	elif value < threshold and threshold != 0 and value >= 0:
		return 1 - (float(value)/threshold)
	else:
		print "error in step function, I was passed a negative value"
		return 0

#species class
class species:
	def __init__(self, number, patch):
		self.population = 50
		#what patch is the species in
		self.patch = patch
		#which number in that patch
		self.number = number
		#what organelles does that species have
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
		#action is between -1 and 1 and is how much you want to increase that compound
		self.compounds_free_action = {}
		#thresholds are the levels at which you are happy with the amount of that compound
		self.compounds_free_thresholds = {}
		self.compounds_locked = {}
		for compound in compounds:
			self.compounds_free[str(compound)] = random.randint(5,25)
			self.compounds_locked[str(compound)] = 10
			#[level at which less is too low, level at which more is too high, vent level]
			self.compounds_free_thresholds[str(compound)] = [10,20,30]
		#setup the cell wall, permeability 0 means no transport, 1 means total transport
		self.permeability = permeability
		#rate at which the species dies a non-predation death
		self.death_rate = 0.05
		#rate at which free compounds are stored as compounds locked and the species grows
		self.growth_rate = 0.1
		#what is the cell made of? (sum of what the organelles are made of)
		self.made_of = {}
		for compound in compounds:
			self.made_of[str(compound)] = 0
		self.compute_made_of()
		#set surface area
		self.surface_area = 50
		self.compute_surface_area()
		#pick a colour for your graph
		self.colour = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]

	#compute the action of each chemical
	def compute_action(self):
		for compound in compounds:
			self.compounds_free_action[str(compound)] = step_function(self.compounds_free[str(compound)], 
				self.compounds_free_thresholds[str(compound)][0], 
				self.compounds_free_thresholds[str(compound)][1],
				self.compounds_free_thresholds[str(compound)][2])

	#for each organelle, for each process that organelle can do, run it
	def run_organelles(self):
		self.compute_action()
		for organelle in self.organelles:
			for process in organelle.processes:
				#calculate the process rate
				input_rate = -1
				output_rate = -1
				for inputs in process.inputs.keys():
					if self.compounds_free_action[str(inputs)] > input_rate:
						input_rate = self.compounds_free_action[str(inputs)]

				for outputs in process.outputs.keys():
					if self.compounds_free_action[str(outputs)] > output_rate:
						output_rate = self.compounds_free_action[str(outputs)]

				#determine how much to act, do nothing if they are both equally far from their optimals
				rate = smoothing_factor*max(output_rate - input_rate,0)
				if rate > 1:
					print "rate = ", rate

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

	#absorb compounds from the environment 
	def absorb(self):
		for compound in compounds:
			if self.compounds_free_action[str(compound)] > 0:
				#work out how much you want
				amount = (self.population*
							self.surface_area*
							permeability[str(compound)]*
							global_absorbtion_factor*
							self.compounds_free_action[str(compound)])

				#take it if you can, otherwise get half
				if self.patch.compounds[str(compound)] <= amount:
					amount = 0.5*self.patch.compounds[str(compound)]

				self.patch.compounds[str(compound)] -= amount
				self.compounds_free[str(compound)] += amount


	#vent any compounds you have too many of
	def vent(self):
		for compound in compounds:
			#if the amount you have is greater than your vent threshold
			if (self.compounds_free[str(compound)] > 
					self.compounds_free_thresholds[str(compound)][2]):
				#work out the difference
				amount = (self.compounds_free[str(compound)] - 
					self.compounds_free_thresholds[str(compound)][2])
				#dump the difference
				self.compounds_free[str(compound)] -= amount
				self.patch.compounds[str(compound)] += amount

	#compute the compunds required to make a new member
	def compute_made_of(self):
		for organelles in self.organelles:
			for compounds in organelles.made_of.keys():
				self.made_of[str(compounds)] += organelles.made_of[str(compounds)]

	#compute the surface area of the species as a whole
	def compute_surface_area(self):
		self.surface_area = math.sqrt(len(self.organelles))

	def compute_population(self):
		pop = 0
		for compound in compounds:
			if self.made_of[str(compound)] > 0:
				pop = self.compounds_locked[(str(compound))]/self.made_of[str(compound)]
		self.population = pop

	#grow new members of the species by moving compounds free -> locked bins
	def grow(self):
		pop_increase = 10000
		for compound in compounds:
			possible_pop_increase = 10000
			if self.made_of[str(compound)] > 0:
				possible_pop_increase = (self.growth_rate*self.compounds_free[str(compound)]/
						self.made_of[str(compound)])
			if possible_pop_increase < pop_increase:
				pop_increase = possible_pop_increase
		#transfer the compounds
		for compound in compounds: 
			self.compounds_free[str(compound)] -= self.made_of[str(compound)]*pop_increase
			self.compounds_locked[str(compound)] += self.made_of[str(compound)]*pop_increase
		self.compute_population()

	def die(self):
		#some of your species die, that means losing compounds to the environment
		for compounds in self.compounds_locked.keys():
			#work out death rate
			amount_to_lose = self.death_rate*self.compounds_locked[str(compounds)]
			#drop compounds
			self.compounds_locked[str(compounds)] -= amount_to_lose
			self.patch.compounds[str(compounds)] += amount_to_lose

#patch class
class patch:
	def __init__(self, number, sunlight = 10):
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

	def run_bacteria(self):
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

	def move_to_optimal(self):
		for compound in compounds:
			difference = self.compounds[str(compound)] - optimals[str(compound)]
			self.compounds[str(compound)] -= 0.01*difference

#initialise
no_species_per_patch = 3
no_of_patches = 2
lower_organelles_per_species = 10
upper_organelles_per_species = 20
smoothing_factor = 0.1 #if the graphs are super spikey then slow down the processes with this
global_absorbtion_factor = 1 # slow down absorbtion with this

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
			if i % 10 == 0:
				percent =  100*float(i)/run_time
				print("%.0f" % percent),
				print "% complete",
				print self.patches[0].compounds
			this_data = []
			for patch in self.patches:
				patch.run_bacteria()
				patch.move_to_optimal()
				patch.compounds["Sunlight"] = 0
				for species in patch.species:
					species.compounds_free["Sunlight"] = patch.sunlight
					species.vent()
					species.run_organelles()
					species.absorb()
					species.grow()
					species.die()
				this_data.append(deepcopy(patch))
				#do accounting
				if i % 10 == 0:
					account = []
					for compound in compounds:
						amount = 0
						amount += patch.compounds[str(compound)]
						for species in patch.species:
							amount += species.compounds_free[str(compound)]
							amount += species.compounds_locked[str(compound)]
						account.append(str(compound) + " : " + str(amount))
					#print account
			self.data.append(this_data)
				
					

