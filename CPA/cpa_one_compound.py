import pygame
import math
import random
from pygame.locals import *
from copy import deepcopy
from copy import copy

#setup

background_colour = (255,255,255)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('One Compound CPA')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

#draw a graph of the species that live in a patch
def display_patch():
	#draw the axes
	pygame.draw.line(screen, [255,0,0], [10, height - 10], [width - 100, height -10], 10)
	pygame.draw.line(screen, [255,0,0], [10, height - 10], [10, 50], 10)
	#plot the compounds
	for species in our_ocean.patches[current_patch].species:
		if locked_or_free == "free":
			#write the label
			label = myfont.render("Patch: " + str(current_patch) + 
				", free compounds", 1, (0,0,0))
			screen.blit(label, [0,0])
			#actually draw the graph
			plot_graph(species.data_free, species.colour)
		if locked_or_free == "locked":
			plot_graph(species.data_locked, species.colour)
			label = myfont.render("Patch: " + str(current_patch) + 
				", locked compounds = population", 1, (0,0,0))
			screen.blit(label, [0,0])

#actual graph plotting function
def plot_graph(data, colour):
	#scale the x and y values so they fit on the graph
	y_scaling = float(height - 100)/max_value
	x_scaling = float(width-180)/len(data)
	current_point = [10,(height - 10) - data[0]*y_scaling]
	#draw lines between the current point and the new point
	for i in range(len(data)):
		new_point = [10 + i*x_scaling, (height - 10) - data[i]*y_scaling]
		pygame.draw.line(screen, colour, current_point, new_point, 5)
		current_point = new_point

#species class
class species:
	def __init__(self, patch, number):
		self.patch = patch
		self.number = number
		#starting values for compounds locked and free
		self.compound_free = random.randint(0,100)
		self.compound_locked = random.randint(0,100)
		#rate at which compounds go from free to locked (growth) and
		#locked to patch (death)
		self.growth_rate = 0.1
		self.death_rate = 0.1
		#your individuals are made up of 1 compound each
		self.population = self.compound_locked
		self.colour = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
		#this stores the historical values so they can be plotted
		self.data_free = []
		self.data_locked = []

	#grow more members by moving compounds from free to locked bin
	def grow(self):
		amount = self.growth_rate*self.compound_free
		self.compound_free -= amount
		self.compound_locked += amount

	#simulate non-predation death by releasing compounds in to the environment
	def die(self):
		amount = self.death_rate*self.compound_locked
		self.compound_locked -= amount
		self.patch.compound += amount 

	#absorb compounds from the environment proportional to your surface area = population
	def absorb(self):
		amount = self.population
		if amount >= self.patch.compound:
			amount = 0.5*self.patch.compound
		self.compound_free += amount
		self.patch.compound -= amount 


#patch class which containst the species and a store of compound
class patch:
	def __init__(self, number):
		self.number = number
		self.species = []
		for i in range(no_of_species_per_patch):
			self.species.append(species(self, i))
		self.compound = 0
		#set the predation relations in the patch
		self.predation_matrix = []
		for i in range(no_of_species_per_patch):
			self.predation_matrix.append([])
			for j in range(no_of_species_per_patch):
				#the diagonals must be zero, a species cannot take from itself
				if j <= i:
					self.predation_matrix[i].append(0)
				#otherwise make something up
				else:
					self.predation_matrix[i].append(random.uniform(-max_predation_rate,max_predation_rate))


	#run the predation in the patch
	def predate(self):
		#basically multiply vector species.locked 
		#by the matrix self.predation_matrix
		new_values = []
		for i in range(no_of_species_per_patch):
			new_values.append(self.species[i].compound_locked)
		for i in range(no_of_species_per_patch):
			for j in range(no_of_species_per_patch):
				if self.predation_matrix[i][j] <= 0:
					amount_to_move = self.predation_matrix[i][j]*new_values[i]
				else:
					amount_to_move = self.predation_matrix[i][j]*new_values[j]
				new_values[i] += amount_to_move
				new_values[j] -= amount_to_move
		for i in range(no_of_species_per_patch):
			self.species[i].compound_locked = new_values[i]

#ocean which contains many patches
class ocean:
	def __init__(self):
		self.patches = []
		for i in range(no_of_patches):
			self.patches.append(patch(i))

#initial variables
no_of_species_per_patch = 5
no_of_patches = 1
run_time = 500
max_predation_rate = 0.1 #this value must be <1/no_of_species 
#and is the %age stolen per timestep
#max value is the highest point on the graph and the one to scale everything else to
max_value = 0

our_ocean = ocean()

for i in range(run_time):
	print i
	#for each patch, for each species grow, die, absord and predate
	for patch in our_ocean.patches:
		patch.predate()
		for species in patch.species:
			species.grow()
			species.die()
			species.absorb()
			#see if there is a new max value which is used in graphing
			if species.compound_locked >= max_value:
				max_value = species.compound_locked
			if species.compound_free >= max_value:
				max_value = species.compound_free
			#store the data for graphing
			species.data_free.append(species.compound_free)
			species.data_locked.append(species.compound_locked)

#display the data 
locked_or_free = "locked"
current_patch = 0
running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	        if event.key == K_UP:
	        	if current_patch < no_of_patches - 1:
	        		current_patch += 1
	        if event.key == K_DOWN:
	        	if current_patch >= 1:
	        		current_patch -= 1
	        if event.key == K_RIGHT:
	        	locked_or_free = "locked"
	        if event.key == K_LEFT:
	        	locked_or_free = "free"
	        


	screen.fill(background_colour)

	display_patch()

	pygame.display.flip()
	

pygame.quit()