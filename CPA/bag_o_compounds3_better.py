#this is a prototype of a bunch of chemicals in a bag
#it can deal with low_thresholds, high_thresholds and vent_thresholds

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

#compute the thresholds of each chemical
def compute_thresholds():
	for i in range(number_of_chemicals):
		thresholds[i] = step_function(chemicals[i], low_threshold[i], 
				high_threshold[i], vent_threshold[i])


chemicals = []
low_threshold = []
high_threshold = []
vent_threshold = []
thresholds = []

number_of_chemicals = 5
run_time = 200

#initialise the chemicals
for i in range(number_of_chemicals):
	chemicals.append(random.randint(0,30))
	low_threshold.append(10)
	high_threshold.append(20)
	vent_threshold.append(30)
	thresholds.append(0)
compute_thresholds()



#initialise the processes
processes = [{"inputs" : [[0,1], [1,1], [2,2]], "outputs" : [[3,1]]},
			{"inputs" : [[3,1]], "outputs" :  [[0,1], [1,1], [2,2]]},
			{"inputs" : [[3,2], [1,2]], "outputs" : [[4,1]]},
			{"inputs" : [[4,1]], "outputs" : [[3,2], [1,2]]}]

#go through the processes, find the inputs and outputs furthest from their optimals
def run_processes():
	for process in processes:
		input_rate = -1
		output_rate = -1
		for inputs in process["inputs"]:
			if thresholds[inputs[0]] > input_rate:
				input_rate = thresholds[inputs[0]]

		for outputs in process["outputs"]:
			if thresholds[outputs[0]] > output_rate:
				output_rate = thresholds[outputs[0]]

		#determine how much to act, do nothing if they are both equally far from their optimals
		rate = max(output_rate - input_rate,0)
		print rate,

		#don't take too much
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

#vent if you are complete stuffed with one compound
def vent():
	for i in range(number_of_chemicals):
		if chemicals[i] > vent_threshold[i]:
			chemicals[i] = vent_threshold[i]

#run the processes and store the result in the data
data = []
max_value = 0
for i in range(run_time):
	print "Reaction rates : ",
	compute_thresholds()
	run_processes()
	vent()
	print "     Chemical quantities : ", chemicals
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


#this loop just waits for user to quit
running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False      

	


	

pygame.quit()