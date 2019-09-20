import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (230,230,230)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Lotka Volterra')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

def draw_axes():
	pygame.draw.line(screen, [200,0,0], [10, height - 110], [width - 150, height - 110], 5)
	pygame.draw.line(screen, [200,0,0], [10, height - 110], [10, 100], 5)

def draw_graph(data, max_value, colour = [0,0,200]):
	time = len(data)
	y_scaling = float(height - 210)/max_value
	x_scaling = float(width-180)/time
	current_point = [10,(height - 110) - data[0]*y_scaling]
	for i in range(len(data)):
		new_point = [10 + i*x_scaling, (height - 110) - data[i]*y_scaling]
		pygame.draw.line(screen, colour, current_point, new_point, 5)
		current_point = new_point
	average = sum(data)/time
	average_point = [10, int((height - 110) - average*y_scaling)]
	pygame.draw.circle(screen, colour, average_point, 10)

def one_species_LV(species):
	species[0] += 0.01*species[0]
	return species

def two_species_LV(species):
	x = species[0]
	y = species[1]
	species[0] += 0.01*(1.1*x - 1.4*x*y)
	species[1] += 0.01*(1.4*x*y - 1.1*y)
	return species

#1. changing p1, p2, p3 will change how good the species are at preying on each other. 
def three_species_LV(species):
	x = species[0]
	y = species[1]
	z = species[2]
	p1 = 0.7
	p2 = 0.3
	p3 = 0.2
	species[0] += 0.01*(1.4*x - p1*x*y - p2*x*z)
	species[1] += 0.01*(p1*x*y - p3*y*z - 0.7*y)
	species[2] += 0.01*(p2*x*z + p3*y*z - 0.7*z)
	return species	

data = [[],[],[]] #this stores historical values for each species
species = [random.uniform(1,2),random.uniform(1,2),random.uniform(1,2)] #this stroes the current pop value of each species

print(species)

running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	       
	#update the equations
	species = three_species_LV(species) #2. choose one_species_LV(species) or two_species_LV(species)
	data[0].append(species[0])
	data[0] = data[0][-1000:]
	data[1].append(species[1])
	data[1] = data[1][-1000:]
	data[2].append(species[2])
	data[2] = data[2][-1000:]

	screen.fill(background_colour)

	colours = [[200,200,0],[0,200,0],[0,0,200]]
	max_value = max(max(data[0]), max(data[1]), max(data[2]))
	draw_axes()
	for d in range(len(data)):
		draw_graph(data[d], max_value, colours[d])

	pygame.display.flip()
	
	#clock.tick(100)  #3. This will slow it down to some FPS, here 100

pygame.quit()