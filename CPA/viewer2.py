import pygame
import math
import random
from pygame.locals import *
from cpa2 import *

#pygame setup
background_colour = (255,255,255)
(width, height) = (1400, 800)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Viewer')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 30)

clock = pygame.time.Clock()

colours = {"Sunlight" : (128,0,0), 
			"Sulfur" : 	(220,150,60), 
			"Hydrogen Sulfide" : (205,92,92),
			"Water" : 	(255,69,0),
			"Oxygen" : 	(50,0,255),
			"Hydrogen" : (0,251,152),
			"Nitrogen" : (143,188,0),
			"Carbon": (0,0,0), 
			"Carbon Dioxide" : (0,0,255), 
			"Glucose" : (0,255,0), 
			"Pyruvate" : (153,0,204), 
			"Protein" : (255,0,203),
			"ATP" : (250,20,100), 
			"Amino Acids" : (255,0,255), 
			"Fat" : (0,158,160), 
			"Ammonia" : (0,205,170), 
			"Agent" : (0,224,208)}

def draw_graph(data, max_value, time, colour = [0,0,255]):
	pygame.draw.line(screen, [255,0,0], [10, height - 110], [width - 150, height - 110], 5)
	pygame.draw.line(screen, [255,0,0], [10, height - 110], [10, 100], 5)
	y_scaling = float(height - 210)/max_value
	x_scaling = float(width-180)/time
	current_point = [10,(height - 110) - data[0]*y_scaling]
	for i in range(len(data)):
		new_point = [10 + i*x_scaling, (height - 110) - data[i]*y_scaling]
		pygame.draw.line(screen, colour, current_point, new_point, 5)
		current_point = new_point

def print_patch_species():
	label = myfont.render("Patch : " + str(current_patch), 1, (0,0,0))
	screen.blit(label, (10, 10))
	label = myfont.render("Species : " + str(current_species), 1, (0,0,0))
	screen.blit(label, (10, 30))

def display_species():
	label = myfont.render("Compounds free in species", 1, (0,0,0))
	screen.blit(label, [width/2,10])
	time = len(ocean.data)
	max_value = 0
	for i in range(time):
		for compounds in ocean.data[i][current_patch].species[current_species].compounds_free.keys():
			value =  ocean.data[i][current_patch].species[current_species].compounds_free[str(compounds)]
			if value >= max_value:
				max_value = value
	for compounds in ocean.data[0][current_patch].species[current_species].compounds_free.keys():
		current_data = []
		for i in range(time):
			current_data.append(ocean.data[i][current_patch].species[current_species].compounds_free[str(compounds)])
		draw_graph(current_data, max_value, time, colours[str(compounds)])

def draw_key():
	y_scaling = int(float(height-20)/len(colours))
	i = 0
	for compounds in colours.keys():
		pygame.draw.line(screen, colours[str(compounds)], [width-10, 10 + i*y_scaling],[width, 10 + i*y_scaling],5)
		label = myfont.render(str(compounds), 1, (0,0,0))
		screen.blit(label, [width-150, 5 + i*y_scaling])
		i += 1

def draw_key2():
	y_scaling = int(float(height-20)/no_of_species_per_patch)
	i = 0
	for species in ocean.data[0][current_patch].species:
		pygame.draw.line(screen, species.colour, [width-10, 10 + i*y_scaling],[width, 10 + i*y_scaling],5)
		label = myfont.render(str(species.number), 1, (0,0,0))
		screen.blit(label, [width-30, 5 + i*y_scaling])
		i += 1

def display_patch():
	label = myfont.render("Compounds free in patch", 1, (0,0,0))
	screen.blit(label, [width/2,10])
	time = len(ocean.data)
	max_value = 0
	for i in range(time):
		for compounds in ocean.data[i][current_patch].compounds.keys():
			value =  ocean.data[i][current_patch].compounds[str(compounds)]
			if value >= max_value:
				max_value = value
	for compounds in ocean.data[0][current_patch].compounds.keys():
		current_data = []
		for i in range(time):
			current_data.append(ocean.data[i][current_patch].species[current_species].compounds_free[str(compounds)])
		draw_graph(current_data, max_value, time, colours[str(compounds)])

def display_patch_pop():
	label = myfont.render("Population in patch", 1, (0,0,0))
	screen.blit(label, [width/2,10])
	time = len(ocean.data)
	max_value = 0
	for i in range(time):
		for species in ocean.data[i][current_patch].species:
			value = species.population
			if value >= max_value:
				max_value = value
	for j in range(len(ocean.data[0][current_patch].species)):
		current_data = []
		for i in range(time):
			current_data.append(ocean.data[i][current_patch].species[j].population)
		draw_graph(current_data, max_value, time, ocean.data[i][current_patch].species[j].colour)



no_of_patches = 1
no_of_species_per_patch = 6
run_time = 20000

ocean = ocean(no_of_patches,no_of_species_per_patch, run_time)

ocean.run_world()


current_patch = 0
current_species = 0
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
	        	if current_species < no_of_species_per_patch - 1:
	        		current_species += 1
	        if event.key == K_LEFT:
	        	if current_species >= -1:
	        		current_species -= 1
	        	

	screen.fill(background_colour)

	print_patch_species()

	if current_species >= 0:
		display_species()
		draw_key()

	if current_species == -1:
		display_patch()
		draw_key()

	if current_species == -2:
		display_patch_pop()
		draw_key2()


	pygame.display.flip()

	clock.tick(60)
	        
pygame.quit()