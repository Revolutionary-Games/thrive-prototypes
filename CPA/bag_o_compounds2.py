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

number_of_chemicals = 5
run_time = 200

#initialise the chemicals
for i in range(number_of_chemicals):
	chemicals.append(random.randint(0,30))
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
processes = [{"inputs" : [[0,1], [1,1], [2,2]], "outputs" : [[3,1]]},
			{"inputs" : [[3,1]], "outputs" :  [[0,1], [1,1], [2,2]]},
			{"inputs" : [[3,2], [1,2]], "outputs" : [[4,1]]},
			{"inputs" : [[4,1]], "outputs" : [[3,2], [1,2]]}]

def run_processes():
	for process in processes:
		input_rate = 0
		output_rate = 0
		for inputs in process["inputs"]:
			temp_input_rate = step_function(chemicals[inputs[0]],low_threshold[inputs[0]])
			if temp_input_rate > input_rate:
				input_rate = temp_input_rate

		for outputs in process["outputs"]:
			temp_output_rate = step_function(chemicals[outputs[0]],low_threshold[outputs[0]])
			if temp_output_rate > output_rate:
				output_rate = temp_output_rate

		rate = max(output_rate - input_rate,0)
		print rate,

		will_run = True
		for inputs in process["inputs"]:
			if chemicals[inputs[0]] < rate*inputs[1]:
				will_run = False
				print "failed to run"

		if will_run:
			for inputs in process["inputs"]:
				chemicals[inputs[0]] -= rate*inputs[1]
			for outputs in process["outputs"]:
				chemicals[outputs[0]] += rate*outputs[1]

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