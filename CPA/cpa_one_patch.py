#prototype for CPA in a single patch
import math
import random
import copy

#Actual simulation

#list of compounds
compounds = ["Sunlight", "Sulfur", "Hydrogen Sulfide", "Oxygen", "Nitrogen",
			"Carbon Dioxide", "Phosphates", "Glucose", "Pyruvate", "Protein",
			"ATP", "Amino Acid", "Fat", "Ammonia", "Agent", "Nucleotide", "DNA"]

#what is the background level in the ocean of these compounds? 
#the player should alter these before playing
ocean_values = {"Sunlight" : 100, "Sulfur" : 0, "Hydrogen Sulfide" : 0, "Oxygen" : 100, 
			"Nitrogen" : 100, "Carbon Dioxide" : 100, "Phosphates" : 100, "Glucose" : 0,
			"Pyruvate" : 0, "Protein" : 0, "ATP" : 0, "Amino Acid" : 0, "Fat" : 0, 
			"Ammonia" : 100, "Agent" : 0, "Nucleotide" : 0, "DNA" : 0}

#allows control over which compounds can pass through the cell boundary
permeability = {"Sunlight" : 1, "Sulfur" : 1, "Hydrogen Sulfide" : 1, "Oxygen" : 1, 
			"Nitrogen" : 1, "Carbon Dioxide" : 1, "Phosphates" : 1, "Glucose" : 1,
			"Pyruvate" : 1, "Protein" : 1, "ATP" : 1, "Amino Acid" : 1, "Fat" : 1, 
			"Ammonia" : 1, "Agent" : 1, "Nucleotide" : 1, "DNA" : 1}

#initialise
no_species_per_patch = 5
#this is the number of copies for auto-evo to use when evaluating the 1 patch!
no_of_patches = 5
#how many organelles should the species have when they spawn?
lower_organelles_per_species = 5
upper_organelles_per_species = 20
smoothing_factor = 0.1 #if the graphs are super spikey then slow down the processes with this
global_absorbtion_factor = 100 # slow down absorbtion with this
ocean_changes = False #can the species change the ocean_values over time?
relative_mass_of_ocean = 0.000001 #how fast should the ocean change?
rate_of_convergence_to_ocean = 1 #how fast (from 0 to 1) should the patch mix with the ocean? 
length_of_sim = 2000 #number of steps to advance when you press the space bar
repetitions_to_do_bettwen_spacebar = 400 #how many times should the sim be repeated?
predation_waste = 0.2 #percentage of compounds lost to the environment (between 0 and 1)
predation_scaling = 0.01 #the smaller this number is the less predation will take place
speed_scaling = 5 # the smaller this number is the less effective speed is at reducing predation
diagnostics = False #print extra info on what is going on?
diagnostics_2 = False #print info on every process run!

LYSOSOME_RATE = 0.6

#turn on or off different processes
predation = True
auto_evo = True

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

processes["Chemosynthesis"] = process("Chemosynthesis", 
						{"Carbon Dioxide" : 6, "Hydrogen Sulfide" : 12},
						{"Glucose" : 1, "Sulfur" : 12})

processes["Photosynthesis"] = process("Photosynthesis", 
						{"Carbon Dioxide" : 6, "Sunlight" : 1},
						{"Glucose" : 1, "Oxygen" : 6})

processes["Glycolysis"] = process("Glycolysis", 
						{"Glucose" : 1},
						{"Pyruvate" : 2, "ATP" : 2})

processes["Respiration"] = process("Respiration", 
						{"Pyruvate" : 1, "Oxygen" : 3},
						{"Carbon Dioxide" : 3, "ATP" : 18})

processes["Sulfur Respiration"] = process("Sulfur Respiration", 
						{"Pyruvate" : 1, "Sulfur" : 3},
						{"Carbon Dioxide" : 3, "Hydrogen Sulfide" : 3, "ATP" : 8})

processes["Protein Synthesis"] = process("Protein Synthesis", 
						{"Amino Acid" : 1, "ATP" : 4},
						{"Protein" : 1})

processes["Protein Digestion"] = process("Protein Digestion", 
						{"Protein" : 1},
						{"Amino Acid" : 1})

processes["Amino Acid Synthesis"] = process("Amino Acid Synthesis", 
						{"Pyruvate" : 1, "ATP" : 3, "Ammonia" : 1},
						{"Amino Acid" : 1})

processes["Amino Acid Digestion"] = process("Amino Acid Digestion", 
						{"Amino Acid" : 1},
						{"Pyruvate" : 1, "ATP" : 2, "Ammonia" : 1})

processes["Fat Synthesis"] = process("Fat Synthesis", 
						{"Pyruvate" : 9, "ATP" : 56},
						{"Fat" : 1, "Carbon Dioxide" : 9})

processes["Fat Digestion"] = process("Fat Digestion", 
						{"Fat" : 1},
						{"Pyruvate" : 6, "ATP" : 45})

processes["Nucleotide Synthesis"] = process("Nucleotide Synthesis", 
						{"Glucose" : 1, "Phosphates" : 1, "ATP" : 8, "Amino Acid" : 2},
						{"Nucleotide" : 1})

processes["Nucleotide Digestion"] = process("Nucleotide Digestion", 
						{"Nucleotide" : 1},
						{"Glucose" : 1, "Phosphates" : 1,"Amino Acid" : 2})

processes["Agent Synthesis"] = process("Agent Synthesis", 
						{"Protein" : 1, "ATP" : 5},
						{"Agent" : 1})

processes["Agent Digestion"] = process("Agent Digestion", 
						{"Agent" : 1},
						{"Amino Acid" : 1})

processes["DNA Synthesis"] = process("DNA Synthesis", 
						{"Nucleotide" : 1, "ATP" : 5},
						{"DNA" : 1})

processes["DNA Digestion"] = process("DNA Digestion", 
						{"DNA" : 1},
						{"Nucleotide" : 1})

processes["Nitrogen Fixation"] = process("Nitrogen Fixation", 
						{"Nitrogen" : 1, "ATP" : 16},
						{"Ammonia" : 2})

processes["Denitrification"] = process("Denitrification", 
						{"Ammonia" : 2,},
						{"Nitrogen" : 2, "ATP" : 10})


#organelles class
class organelle:
	def __init__(self, name, processes, made_of, maintenance = 0.12):
		self.name = name
		#what processes the organelle can do
		self.processes = processes
		#what the organelle is made of 
		self.made_of = made_of
		self.maintenance = maintenance

#all the organelles
organelles = {}

organelles["Chemoplast"] = organelle("Chemoplast", 
				[processes["Chemosynthesis"]],
				{"Protein" : 2, "Fat" : 1})

organelles["Chloroplast"] = organelle("Chloroplast", 
				[processes["Photosynthesis"]],
				{"Protein" : 2, "Fat" : 1})

organelles["Cytoplasm"] = organelle("Cytoplasm", 
				[processes["Glycolysis"],
				processes["Fat Synthesis"],
				processes["Fat Digestion"],
				processes["Amino Acid Synthesis"],
				processes["Amino Acid Digestion"]],
				{"Protein" : 2, "Fat" : 1})

organelles["Mitochondria"] = organelle("Mitochondria", 
				[processes["Respiration"]],
				{"Protein" : 2, "Fat" : 1})

organelles["Sulfur Mitochondria"] = organelle("Sulfur Mitochondria", 
				[processes["Sulfur Respiration"]],
				{"Protein" : 2, "Fat" : 1})

organelles["Agent Gland"] = organelle("Agent Gland", 
				[processes["Agent Synthesis"]],
				{"Protein" : 2, "Fat" : 1})

organelles["Nucleus"] = organelle("Nucleus", 
				[processes["Nucleotide Synthesis"],
				processes["DNA Synthesis"],
				processes["Protein Synthesis"]],
				{"Protein" : 2, "Fat" : 1, "DNA" : 1})

organelles["Lysosomes"] = organelle("Lysosomes", 
				[processes["Protein Digestion"],
				processes["Nucleotide Digestion"],
				processes["DNA Digestion"],
				processes["Agent Digestion"]],
				{"Protein" : 2, "Fat" : 1})

organelles["Flagella"] = organelle("Flagella", 
				[],
				{"Protein" : 2, "Fat" : 1},
				0.48)

organelles["Pilus"] = organelle("Pilus", 
				[],
				{"Protein" : 2, "Fat" : 1})

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

#this function takes the strengths of the two species and returns the rate of predation between them
#at the moment it is super simple as this whole concept needs work
#it should be anti-symmetric so (1,2) = -(2,1) as the flow is the same but opposite
#it should return a value between 0 and 1 but 1 means transfer ALL compounds per time step
#this function should return predation from species_1 to species_2!
def compute_predation(species_1, species_2):
	strength_difference = species_2.strength - species_1.strength
	strength_difference_sign = math.copysign(1, strength_difference)
	predation = strength_difference_sign*(1 - math.exp(-abs(strength_difference)*predation_scaling))
	#compute the speed reduction factor
	#if one of the species is faster it can choose to run rather than fight and get a discount
	speed_difference = species_2.speed - species_1.speed
	#the discount should be a value between 0 and 1
	speed_discount = math.exp(-speed_scaling*abs(speed_difference))
	#work out whether to apply the discount based on which species is gaining from the predation
	#case: if compounds are going from 1 -> 2 and 1 is faster
	if predation >= 0 and speed_difference <= 0:
		predation *= speed_discount
	#case: if compounds are going from 2 -> 1 and species 2 is faster
	elif predation < 0 and speed_difference >= 0:
		predation *= speed_discount
	return predation

#count the number of organelles of a certain type
def count_organelles(species, name):
	count = 0
	for organ in species.organelles:
		if organ.name == name:
			count += 1
	return count

#keep track of which variations have already been tried
organelles_added = []
organelles_subtracted = []

#this function chooses whether to add or subtract an organelle, it's part of auto-evo
def add_or_subtract_organelle(species):
	#keep track of which organelles are already being tested
	global organelles_added
	global organelles_subtracted
	#randomly choose whether to add or subtract
	#always choose to add if the only organelles remaining are nucleus and cytoplasm
	#always choose to add if all possible subtractions are already being tried
	if (random.choice([True, False]) or len(species.organelles) <= 2 or
		len(species.organelles) - len(organelles_subtracted) <= 2):
		#add an organelle
		choice = False
		fail_counter = 0
		while 1:
			choice = random.choice(organelles.keys())
			#you can't add another nucleus
			if choice != "Nucleus" and choice not in organelles_added:
				species.organelles.append(organelles[str(choice)])
				print " adding ", str(choice)
				organelles_added.append(choice)
				break

			fail_counter += 1
			if fail_counter >= 100:
				print "Failed to add an organelle!"
				break

	else:
		#subtract an organelle
		fail_counter = 0
		choice = False
		while 1:

			choice = random.choice(species.organelles)
			#you can't take away the nucleus
			if choice.name != "Nucleus" and choice.name != "Cytoplasm" and choice.name not in organelles_subtracted:
				species.organelles.remove(choice)
				print " removing ", str(choice.name)
				organelles_subtracted.append(choice.name)
				break
			#you can only take away cytoplasm if 2 or more remain
			elif (choice.name != "Nucleus" and count_organelles(species, "Cytoplasm") >= 2 and
				choice.name not in organelles_subtracted):
					species.organelles.remove(choice)
					organelles_subtracted.append(choice)
					print " removing ", str(choice.name)
					break

			fail_counter += 1
			if fail_counter >= 100:
				print "Failed to subtract an organelle!"
				break

#this function prints the current state of the patch
def print_current_state(patch):
	print "Current State: F = Flagella, A = Agents, P = Pilli, C = Chloroplast,",
	print "Y = Cytoplasm, L = Lysosomes, M = Mitochondria, T = Total number of organelles,",
	print "O = Population:"
	for specie in patch.species:
		print "F :", count_organelles(specie, "Flagella"),
		print " A :", count_organelles(specie, "Agent Gland"),
		print " P :", count_organelles(specie, "Pilus"),
		print " C :", count_organelles(specie, "Chloroplast"),
		print " Y :", count_organelles(specie, "Cytoplasm"),
		print " L :", count_organelles(specie, "Lysosomes"),
		print " M :", count_organelles(specie, "Mitochondria"),
		print " T :", len(specie.organelles),
		print " O :", specie.average_population,
		print "."

#species class
class species:
	def __init__(self, number, patch):
		#starter population
		self.population = 50
		#list of 50 past population numbers
		self.population_memory = []
		#average population over the last 50 steps
		self.average_population = 0
		#what patch is the species in
		self.patch = patch
		#which number in that patch
		self.number = number
		#what organelles does that species have
		self.organelles = []
		self.organelles_old = [] #a list of the organelles a species had before the last autoevo
		#add organelles to the species, make sure there is only 1 nucleus
		number_of_organelles = 0#random.randint(lower_organelles_per_species, upper_organelles_per_species)
		while number_of_organelles > 0:
			choice = random.choice(organelles.keys())
			if choice != "Nucleus":
				self.organelles.append(organelles[str(choice)])
				number_of_organelles -= 1
		#the minimum viable species has Nuleus + Cytoplasm
		self.organelles.append(organelles["Chloroplast"])
		self.organelles.append(organelles["Cytoplasm"])
		self.organelles.append(organelles["Nucleus"])
		self.organelles_old = self.organelles[:]
		#setup the compounds bins
		self.compounds_free = {}
		#action is between -1 and 1 and is how much you want to increase that compound
		self.compounds_free_action = {}
		#thresholds are the levels at which you are happy with the amount of that compound
		self.compounds_free_thresholds = {}
		self.compounds_locked = {}
		self.compounds_locked_old = {}
		self.compounds_food = {}
		for compound in compounds:
			self.compounds_free[str(compound)] = random.randint(5,25)
			self.compounds_locked[str(compound)] = 100
			self.compounds_food[str(compound)] = 0
			self.compounds_locked_old[str(compound)] = 0
			#[level at which less is too low, level at which more is too high, vent level]
			self.compounds_free_thresholds[str(compound)] = [10,20,30]
		#setup the cell wall, permeability 0 means no transport, 1 means total transport
		self.permeability = permeability
		#rate at which the species dies a non-predation death
		self.death_rate = 0.00001
		#rate at which free compounds are stored as compounds locked and the species grows
		self.growth_rate = 0.5
		#what is the cell made of? (sum of what the organelles are made of)
		self.made_of = {}
		self.made_of_old = {}
		for compound in compounds:
			self.made_of[str(compound)] = 0
			self.made_of_old[str(compound)] = 0
		self.compute_made_of()
		self.compute_made_of()
		#set surface area
		self.surface_area = 0
		self.compute_surface_area()
		#pick a colour for your species
		self.colour = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
		#set a strength for the species, this needs to be done intelligently
		self.strength = 0
		self.compute_fight_strength()
		#set a speed value for the species
		self.speed = 0
		self.compute_speed()

	#compute the speed of the species
	def compute_speed(self):
		number_of_flagella = 0
		for organelle in self.organelles:
			if organelle.name == "Flagella":
				number_of_flagella += 1 
		self.speed = float(number_of_flagella)/float(len(self.organelles))
	
	#compute the fight strength of the species
	def compute_fight_strength(self):
		self.strength = 0
		for organelle in self.organelles:
			if organelle.name == "Pilus":
				self.strength += 1
			if organelle.name == "Agent Gland":
				self.strength += 2

	#compute the action of each chemical
	def compute_action(self):
		for compound in compounds:
			self.compounds_free_action[str(compound)] = step_function(self.compounds_free[str(compound)],
				self.compounds_free_thresholds[str(compound)][0],
				self.compounds_free_thresholds[str(compound)][1],
				self.compounds_free_thresholds[str(compound)][2])

	#for each organelle, for each process that organelle can do, run it
	def run_organelles(self):
		#work out where the value is relative the thresholds for that compound
		self.compute_action()
		for organelle in self.organelles:
			if organelle.name == "Lysosomes":
				ctemp = [c for c in compounds]
				for process in organelle.processes:
					# Lysosome will always try to process as much as it can
					c0 = process.inputs.keys()[0]
					rate = self.compounds_food[str(c0)]/ process.inputs[c0]
					for inputs in process.inputs.keys():
						rate = min(rate, self.compounds_food[str(inputs)] / process.inputs[inputs])
					rate *= LYSOSOME_RATE
					for compounds in process.inputs.keys():
						ctemp.remove(compunds)
						self.compounds_food[str(compounds)] -= rate*process.inputs[str(compounds)]
					for compounds in process.outputs.keys():
						self.compounds_free[str(compounds)] += rate*process.outputs[str(compounds)]
				for c in ctemp:
					amt = self.compounds_food[c]
					self.compounds_food[c] = 0
					self.compounds_free[c] += amt
				continue
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
				rate = smoothing_factor*max(output_rate - input_rate,0)*self.population
				#print any errors
				#if rate > 1:
				#	print "rate = ", rate

				#check there are enough inputs
				if self.number is 0 and self.patch.number is 0 and diagnostics_2:
					print process.name, "Wanted", rate,
				will_run = False
				counter = 0
				while not will_run and counter <= 1000:
					passed_tests = True
					for compounds in process.inputs.keys():
						if rate*process.inputs[str(compounds)] >= self.compounds_free[str(compounds)]:
							passed_tests = False
					if passed_tests:
						will_run = True
					counter += 1
					rate *= 0.9
				#run the process
				if will_run:
					for compounds in process.inputs.keys():
						self.compounds_free[str(compounds)] -= rate*process.inputs[str(compounds)]
					for compounds in process.outputs.keys():
						self.compounds_free[str(compounds)] += rate*process.outputs[str(compounds)]

				#print diagnostics for this process
				if self.number is 0 and self.patch.number is 0 and diagnostics_2:
					print "got", rate
		if self.number is 0 and self.patch.number is 0 and diagnostics_2:
			print self.compounds_free

	#absorb compounds from the environment 
	def absorb(self):
		for compound in compounds:
			if self.compounds_free_action[str(compound)] > 0:
				#work out how much you want
				amount = (permeability[str(compound)]*
							global_absorbtion_factor*
							self.compounds_free_action[str(compound)])

				#take it if you can, otherwise get half of what there is available
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
		#store the current values in the old list
		self.made_of_old = dict(self.made_of)
		#reset the values
		for compound in compounds:
			self.made_of[str(compound)] = 0
		#ask each organelle what is made of
		for organelles in self.organelles:
			for compound in organelles.made_of.keys():
				#add this value to the total
				self.made_of[str(compound)] += organelles.made_of[str(compound)]

	#compute the surface area of the species as a whole
	def compute_surface_area(self):
		self.surface_area = math.sqrt(len(self.organelles))

	#compute the size of the population of the species
	def compute_population(self):
		pop = 0
		pop_old = 0
		for compound in compounds:
			if self.made_of[str(compound)] > 0:
				pop = self.compounds_locked[(str(compound))]/self.made_of[str(compound)]
			if self.made_of_old[str(compound)] > 0:
				pop_old = self.compounds_locked_old[(str(compound))]/self.made_of_old[str(compound)]
		self.population = pop + pop_old
		#keep a list of the last 50 values (to smooth out rapid oscillations)
		self.population_memory.append(self.population)
		if len(self.population_memory) > 50:
			self.population_memory.pop(0)
		if self.number == 0 and diagnostics:
			print "Old and new Populations for species number : ", self.number, "pop", pop, "pop_old ", pop_old, "tot", self.population

	#work out the average population over the last 50 steps
	def compute_average_population(self):
		if len(self.population_memory) > 0:
			self.average_population = float(sum(self.population_memory))/len(self.population_memory)
		else:
			print "Error: Population_Memory is length 0!"

	def maintenance(self):
		maintenance = 0
		for organelle in self.organelles:
			maintenance += organelle.maintenance
		maintenance /= len(self.organelles)
		self.compounds_free["ATP"] -=  self.population * maintenance
		if self.compounds_free["ATP"] < 0: self.compounds_free["ATP"] = 0

	def recalculate_free_thresholds(self):
		for compound in compounds:
			self.compounds_free_thresholds[str(compound)] = [
				10 * (1 + self.population * len(self.organelles)),
				20 * (1 + self.population * len(self.organelles)),
				30 * (1 + self.population * len(self.organelles))
			]

	#grow new members of the species by moving compounds free -> locked bins
	def grow(self):
		pop_increase = 10000
		for compound in compounds:
			possible_pop_increase = 10000
			#work out which compound is the limiting one
			if self.made_of[str(compound)] > 0:
				possible_pop_increase = (float(self.growth_rate*self.compounds_free[str(compound)])/
						self.made_of[str(compound)])
			if possible_pop_increase < pop_increase:
				pop_increase = possible_pop_increase
		#transfer the compounds
		for compound in compounds: 
			self.compounds_free[str(compound)] -= self.made_of[str(compound)]*pop_increase
			self.compounds_locked[str(compound)] += self.made_of[str(compound)]*pop_increase

	def die(self):
		#some of your species die, that means losing compounds to the environment
		for compound in compounds:
			#work out death rate
			amount_to_lose = self.death_rate*self.compounds_locked[str(compound)]
			#drop compounds
			self.compounds_locked[str(compound)] -= amount_to_lose
			self.patch.compounds[str(compound)] += amount_to_lose
			#work out death rate
			amount_to_lose = self.death_rate*self.compounds_locked_old[str(compound)]
			#drop compounds
			self.compounds_locked_old[str(compound)] -= amount_to_lose
			self.patch.compounds[str(compound)] += amount_to_lose
		self.compute_population()


#patch class
class patch:
	def __init__(self, number):
		self.number = number
		#put some species in each patch
		self.species = []
		for i in range(no_species_per_patch):
			self.species.append(species(i, self))
		#compute the predation relations
		self.predation_relations = []
		self.compute_predation_relations()
		#set environmental compounds
		self.compounds = dict(ocean_values)

	def compute_predation_relations(self):
		self.predation_relations = []
		#make a sqaure matrix of the right size
		for i in range(no_species_per_patch):
			self.predation_relations.append([])
			for j in range(no_species_per_patch):
				#only put entries in the upper diagonal
				if i >= j:
					self.predation_relations[i].append(0)
				#otherwise add an entry to the matrix
				else:
					self.predation_relations[i].append(
						compute_predation(self.species[i], self.species[j]))

	#move compunds based on the predation relations
	def run_predation(self):
		#the list of actions should be randomised because whoever gets the first move gets more
		#because each species takes a %age of the total so if the first species gets 5% of 1
		#then the second species gets 5% of 0.95 even though they are supposed to get the same
		list_of_predations = []
		total_patch_population = 0
		for specie in self.species:
			total_patch_population += specie.population
		for i in range(no_species_per_patch):
			for j in range(no_species_per_patch):
				population_densities = float(self.species[i].population*
					self.species[j].population)/(total_patch_population**2)
				amount_to_move = self.predation_relations[i][j]*population_densities
				list_of_predations.append([i,j,amount_to_move])

		random.shuffle(list_of_predations)

		for predation in list_of_predations:
			self.move_compounds(predation[0], predation[1], predation[2])

	#take compounds from the prey and give them to the predator
	def move_compounds(self, i,j,amount):

		for compound in compounds:
			#you get amount% of their free and locked bins, whose bin it is matters			
			if amount >= 0:
				amount_to_move_free = amount*self.species[i].compounds_free[str(compound)]
				self.species[i].compounds_free[str(compound)] -= amount_to_move_free
				self.species[j].compounds_food[str(compound)] += (1 - predation_waste)*amount_to_move_free
				self.compounds[str(compound)] += predation_waste*amount_to_move_free
				#amount_to_move_locked = amount*self.species[i].compounds_locked[str(compound)]
			else:
				amount_to_move_free = -amount*self.species[j].compounds_free[str(compound)]
				self.species[j].compounds_free[str(compound)] -= amount_to_move_free
				self.species[i].compounds_food[str(compound)] += amount_to_move_free * (1 - predation_waste)
				self.compounds[str(compound)] += predation_waste*amount_to_move_free
				#amount_to_move_locked = amount*self.species[j].compounds_locked[str(compound)]
			#do it for compounds free
			#self.species[i].compounds_free[str(compound)] -= amount_to_move_free
			#self.species[j].compounds_free[str(compound)] += amount_to_move_free
			#self.compounds[str(compound)] += predation_waste*amount_to_move_free
			#and compounds locked
			#amount_to_move = amount*self.species[i].compounds_locked[str(compound)]
			#self.species[i].compounds_locked[str(compound)] -= amount_to_move_locked
			#self.species[j].compounds_free[str(compound)] += amount_to_move_locked

	#mix the patch with the ocean, control with "rate_of_convergence to ocean" and "relative _mass_of_ocean"
	def move_to_optimal(self):
		global ocean_values
		for compound in compounds:
			difference = self.compounds[str(compound)] - ocean_values[str(compound)]
			self.compounds[str(compound)] -= rate_of_convergence_to_ocean*difference
			if ocean_changes:
				ocean_values[str(compound)] += rate_of_convergence_to_ocean*relative_mass_of_ocean*difference



#the main class which holds the patches
class ocean:
	def __init__(self):
		#make some patches
		self.patches = []
		for i in range(no_of_patches):
			self.patches.append(patch(i))
		self.data = []
		#which species is auto-evo mutating
		self.species_under_auto_evo = 0
		#keep track of how many steps have passed
		self.time = 0

	#advance the simultion by one time step
	def run_world(self):
		for patch in self.patches:
			#mix the ocean and the patch a little
			patch.move_to_optimal()
			#for each species run their different processes
			for species in patch.species:
				species.maintenance()
				species.vent()
				species.run_organelles()
				species.absorb()
				species.grow()
				species.die()
				species.recalculate_free_thresholds()
			#run the predation in the patch
			if predation:
				patch.run_predation()
		self.time += 1

	#Auto-evo!
	def auto_evo(self):
		#choose the most successful mutation from the last round
		max_pop = 0
		best_version = 0
		print "The resulting populations are : "
		for i in range(len(self.patches)):
			#tell the species to compute it's average population over the last 50 steps
			for specie in self.patches[i].species:
				specie.compute_average_population()
			print " ", i, ":", self.patches[i].species[self.species_under_auto_evo].average_population,
			#if that pop is greater than the current best then make it the current best
			if self.patches[i].species[self.species_under_auto_evo].average_population >= max_pop:
				max_pop = self.patches[i].species[self.species_under_auto_evo].average_population
				best_version = i
		print "."
		print "The best version was in patch ", best_version, " with average population ", max_pop
		#make a list for the new patches to go in (which are copies of the best patch)
		new_patches = []
		new_patches.append(self.patches[best_version])
		self.patches = new_patches
		#switch the current blueprint to the old blueprint, switch the locked bin to old locked bin
		for specie in self.patches[0].species:
			#first empty the old compounds locked bin
			for compound in compounds:
				amount = specie.compounds_locked_old[str(compound)]
				specie.compounds_locked_old[str(compound)] -= amount
				self.patches[0].compounds[str(compound)] += amount
			#then move the current locked into the old locked array
			specie.compounds_locked_old = dict(specie.compounds_locked)
			#then zero the compounds locked
			for compound in compounds:
				specie.compounds_locked[str(compound)] = 0
		#copy the patch 5 times for new mutations to be tested
		for i in range(no_of_patches - 1):
			self.patches.append(copy.deepcopy(self.patches[0]))
		for i in range(no_of_patches):
			self.patches[i].number = i
		#print the current state
		print_current_state(self.patches[0])
		#reset the list of choices which have already been tried.
		global organelles_added
		global organelles_subtracted
		organelles_added = []
		organelles_subtracted = []		
		#choose a species to be mutated
		self.species_under_auto_evo = random.randint(0, no_species_per_patch - 1)
		print "Mutation will be applied to species ", self.species_under_auto_evo
		print "Patch 0 will be the control."
		for i in range(1,len(self.patches)):
			print "In patch ", str(i), 
			add_or_subtract_organelle(self.patches[i].species[self.species_under_auto_evo])
		for i in range(len(self.patches)):
			#compute the new attributes of the species which has been altered
			self.patches[i].species[self.species_under_auto_evo].compute_fight_strength()
			self.patches[i].species[self.species_under_auto_evo].compute_speed()
			self.patches[i].species[self.species_under_auto_evo].compute_made_of()
			self.patches[i].species[self.species_under_auto_evo].compute_surface_area()
			if diagnostics:
				print "mutated species new values",
				print "strength :", self.patches[i].species[self.species_under_auto_evo].strength,
				print "speed :", self.patches[i].species[self.species_under_auto_evo].speed,
				print "made of :", self.patches[i].species[self.species_under_auto_evo].made_of,
				print "surface_area :", self.patches[i].species[self.species_under_auto_evo].surface_area
			#compute the new predation relations in the patch
			self.patches[i].compute_predation_relations()




our_ocean = ocean()


#this is the data which will be drawn
def reset_data():
	global data
	data = []
	for i in range(no_species_per_patch):
		data.append([])
reset_data()

#what to do when space is pressed and the simulation is advanced 
def advance():
	global data
	reset_data()
	steps_per_percent = float(length_of_sim)/100
	print "Percentage Completed : ",
	for i in range(length_of_sim):
		percent_complete = float(i)/steps_per_percent
		if percent_complete % 10 == 0:
			print percent_complete,
		#run the world and collect the data to display
		our_ocean.run_world()
		for j in range(no_species_per_patch):
			data[j].append(our_ocean.patches[0].species[j].population)
	print "done"

	if auto_evo:
		our_ocean.auto_evo()
	else:
		print "Pops :",
		for i in range(no_species_per_patch):
			print our_ocean.patches[0].species[i].population,
		print "."

#main loop, will start immediately
for i in range(repetitions_to_do_bettwen_spacebar):
	print ""
	print "Doing step ", i
	advance()