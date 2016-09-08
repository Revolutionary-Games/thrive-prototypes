import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (255,255,255)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Let there be LIGHT')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

data = [0.10248431224755133, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7975972483713.395, 8202637231969.165, 8031996561524.898, 7611855247979.894, 1531098438830.4739, 1398493715558.7437, 1264759325195.5273, 5237544121350.967, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def draw_graph(data, colour = [0,0,255]):
	#work out the x length of the data
	time = len(data)
	#work out the y region to plot
	max_value = max(data)
	min_value = min(data)
	range_to_plot = max(max_value - min_value,0.1)
	#print min and max values
	label = myfont.render("Max = " + str(max_value) + " Min = " + str(min_value), 1, (0,0,0))
	screen.blit(label, (10, 10))
	#scale the axes and find where to plot zero
	y_scaling = float(height - 210)/range_to_plot
	y_zero = -min_value*y_scaling
	x_scaling = float(width-180)/time
	#draw the axes
	pygame.draw.line(screen, [255,0,0], [10, height - 110 - y_zero], 
		[width - 150, height - 110 - y_zero], 5)
	pygame.draw.line(screen, [255,0,0], [10, height - 110], [10, 100], 5)
	#start with the current point
	current_point = [10,(height - 110) - data[0]*y_scaling - y_zero]
	#draw the data points
	for i in range(len(data)):
		new_point = [10 + i*x_scaling, (height - 110) - data[i]*y_scaling - y_zero]
		pygame.draw.line(screen, colour, current_point, new_point, 5)
		current_point = new_point

screen.fill(background_colour)

draw_graph(data)	

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