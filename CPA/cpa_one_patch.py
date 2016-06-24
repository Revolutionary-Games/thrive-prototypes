#prototype for CPA in a single patch

import pygame
import math
import random
from pygame.locals import *

#setup, just PYGAME stuff and not required.

background_colour = (255,255,255)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('One Patch CPA')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

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
#there must be 5 copies for auto-evo!
no_of_patches = 1
#how many organelles should the species have when they spawn?
lower_organelles_per_species = 10
upper_organelles_per_species = 20
smoothing_factor = 0.1 #if the graphs are super spikey then slow down the processes with this
global_absorbtion_factor = 1 # slow down absorbtion with this
ocean_changes = False #can the species change the ocean_values over time?
relative_mass_of_ocean = 0.000001 #how fast should the ocean change?
rate_of_convergence_to_ocean = 0.01 #how fast (from 0 to 1) should the pax mix with the ocean?

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
	def __init__(self, name, processes, made_of):
		self.name = name
		#what processes the organelle can do
		self.processes = processes
		#what the organelle is made of 
		self.made_of = made_of

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
				{"Protein" : 2, "Fat" : 1, "DNA" : 10})

organelles["Lysosomes"] = organelle("Lysosomes", 
				[processes["Protein Digestion"],
				processes["Nucleotide Digestion"],
				processes["DNA Digestion"],
				processes["Agent Digestion"]],
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

#species class
class species:
	def __init__(self, number, patch):
		#starter population
		self.population = 50
		#what patch is the species in
		self.patch = patch
		#which number in that patch
		self.number = number
		#what organelles does that species have
		self.organelles = []
		#the minimum viable species has Nuleus + Cytoplasm
		self.organelles.append(organelles["Nucleus"])
		self.organelles.append(organelles["Cytoplasm"])
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
			self.compounds_locked[str(compound)] = 100
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
		#pick a colour for your species
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
		#work out where the value is relative the thresholds for that compound
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

				#take it if you can, otherwise get half of what there is availble
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
	def __init__(self, number):
		self.number = number
		#put some species in each patch
		self.species = []
		for i in range(no_species_per_patch):
			self.species.append(species(i, self))
		#set environmental compounds
		self.compounds = dict(ocean_values)

	def move_to_optimal(self):
		global ocean_values
		for compound in compounds:
			difference = self.compounds[str(compound)] - ocean_values[str(compound)]
			self.compounds[str(compound)] -= rate_of_convergence_to_ocean*difference
			if ocean_changes:
				ocean_values[str(compound)] += rate_of_convergence_to_ocean*relative_mass_of_ocean*difference




class ocean:
	def __init__(self):
		#make some patches
		self.patches = []
		for i in range(no_of_patches):
			self.patches.append(patch(i))
		self.data = []

	def run_world(self):
		for patch in self.patches:
			patch.move_to_optimal()
			for species in patch.species:
				species.vent()
				species.run_organelles()
				species.absorb()
				species.grow()
				species.die()

our_ocean = ocean()

#Back to pygame stuff for displaying the data

def draw_graph(data, max_value, colour = [0,0,255]):
	pygame.draw.line(screen, [255,0,0], [10, height - 110], [width - 150, height - 110], 5)
	pygame.draw.line(screen, [255,0,0], [10, height - 110], [10, 100], 5)
	y_scaling = float(height - 210)/max_value
	x_scaling = float(width-180)/len(data)
	current_point = [10,(height - 110) - data[0]*y_scaling]
	for i in range(len(data)):
		new_point = [10 + i*x_scaling, (height - 110) - data[i]*y_scaling]
		pygame.draw.line(screen, colour, current_point, new_point, 5)
		current_point = new_point
	pygame.display.flip()

data = []
for i in range(no_species_per_patch):
	data.append([])
def advance():
	global data
	length_of_sim = 10000
	steps_per_percent = length_of_sim/100
	for i in range(length_of_sim):
		percent_complete = i/steps_per_percent
		if i % steps_per_percent == 0:
			print percent_complete, ": percent complete"
		our_ocean.run_world()
		for j in range(no_species_per_patch):
			if percent_complete >= 10:
				data[j].append(our_ocean.patches[0].species[j].population)
	#for patch in our_ocean.patches:
	#	for species in patch.species:
	#		print patch.number, species.number, species.population,
	#print "Next Step"
	for data_set in data:
		draw_graph(data_set, max(data_set), colour = [random.randint(0,255), random.randint(0,255), random.randint(0,255)])


halt = True
running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	        if event.key == K_SPACE:
	        	advance()

	
	clock.tick(60)

pygame.quit()