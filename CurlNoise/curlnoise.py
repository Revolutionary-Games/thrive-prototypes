# this program generates a 2D fluid vector field from some noise
#the noise isn't very good so the 2D field isn't very good but it does work fine
#2 more things remain to be added
#first a ramp function when you are close to the boundary (psi should decay to zero near any boundaries)
#second there is a formula for moving objects so they leave nice trails
#I'm folling this paper
#http://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph2007-curlnoise.pdf

import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (255,255,255)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Noise')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

scale = 1

time = 0

#calculates the change in the potential psi between two points
def get_derivative(point1, point2):
	return (point2.psi - point1.psi)*10

#class for the points in the grid, i,j are there coordinates, x,y are their positions
class point:
	def __init__(self, i, j):
		self.i = i
		self.j = j
		self.x = 10*i
		self.y = 10*j
		self.psi = 0
		self.dx = 0
		self.dy = 0

	def display(self):
		#pygame.draw.circle(screen, (255,0,0), (int(scale*self.x), int(scale*self.y)), int(scale*1))
		pygame.draw.line(screen, (0,0,255), 
			(int(scale*self.x), int(scale*self.y)), (int(scale*self.x + 2*self.dx), int(scale*self.y + 2*self.dy)), 1)

	#get the vector field from the potential field, turns out it's super simple
	def generate_vector_field(self):
		self.dx = get_derivative(self, points[self.i + 1][self.j])
		self.dy = get_derivative(self, points[self.i][self.j + 1])

	#generate noise for the potential field, this is where I don't really know what I'm doing
	def generate_psi(self):
		noise = (math.sin(self.i/3 + time)*math.cos(self.j/3 + time))
		#noise = math.sqrt((50 + time - i)**2 + (50 + time - j)**2)
		self.psi = noise


#initialise
points = []

x_size = 100
y_size = 100

for i in range(x_size):
	points.append([])
	for j in range(y_size):
		points[i].append(point(i,j))




running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN: 
	        if event.key == K_ESCAPE:
	            running = False

	screen.fill(background_colour)

	#generate the potential field and from it the vector field
	for i in range(x_size - 1):
		for j in range(y_size - 1):
			points[i][j].generate_psi()
			points[i][j].generate_vector_field()

	#display
	for i in range(len(points)):
		for j in range(len(points[i])):
			points[i][j].display()

	time += 0.5
	if time >= 3*math.pi:
		time = 0

	pygame.display.flip()

pygame.quit()