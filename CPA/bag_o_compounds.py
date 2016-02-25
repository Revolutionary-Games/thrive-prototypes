#this is a prototype of a bunch of chemicals in a bag

import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (255,255,255)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Chemicals in a bag')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

#draw the graph on the screen, not conceptually important
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

#compute the concentrations of each chemical
def compute_concentrations():
	total = sum(chemicals)
	if total > 0:
		for i in range(number_of_chemicals):
			concentrations[i] = float(chemicals[i])/total

chemicals = []
low_threshold = []
concentrations = []

number_of_chemicals = 2
run_time = 100

#initialise the chemicals
for i in range(number_of_chemicals):
	chemicals.append(random.randint(0,3))
	low_threshold.append(10)
	concentrations.append(0)
compute_concentrations()

#create a step function
def step_function(value, threshold):
	if value >= threshold:
		return 0
	elif value < threshold and threshold != 0 and value >= 0:
		return 1 - (float(value)/threshold)
	else:
		print "error in step function"
		return 0

#initialise the processes
processes = [[0,1],[1,0]]

def run_processes():
	for process in processes:
		rate = step_function(chemicals[process[1]], low_threshold[process[1]])
		if chemicals[process[0]] > rate:
			chemicals[process[0]] -= rate
			chemicals[process[1]] += rate
		else:
			rate = float(chemicals[process[0]])/2
			chemicals[process[0]] -= rate
			chemicals[process[1]] += rate

#run the processes and store the result in the data
data = []
max_value = 0
for i in range(run_time):
	compute_concentrations()
	run_processes()
	print chemicals
	data.append(chemicals[:])
	for j in range(number_of_chemicals):
		if chemicals[j] >= max_value:
			max_value = chemicals[j]

#draw all the graphs
screen.fill(background_colour)

for i in range(number_of_chemicals):
	plot = []
	for j in range(run_time):
		plot.append(data[j][i])
	draw_graph(plot, max_value, run_time, [(100*i) % 255, (150*i) % 255, (225*i) % 255])

pygame.display.flip()



running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	       

	


	

pygame.quit()