# this program generates a 2D fluid vector field from some noise
#the noise isn't very good so the 2D field isn't very good but it does work fine
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
		self.ramp = 0
		self.in_wake = 0
		self.dx = 0
		self.dy = 0

	def display(self):
		#pygame.draw.circle(screen, (255,0,0), (int(scale*self.x), int(scale*self.y)), int(scale*1))
		pygame.draw.line(screen, (0,0,255), 
			(int(scale*self.x), int(scale*self.y)), (int(scale*self.x + 2*self.dx), int(scale*self.y + 2*self.dy)), 1)

	#get the vector field from the potential field, turns out it's super simple
	def generate_vector_field(self):
		self.dy = -get_derivative(self, points[self.i + 1][self.j])
		self.dx = get_derivative(self, points[self.i][self.j + 1])

	#if you are close to the boundary scale the potential down to zero the closer you get
	def set_ramp(self):
		distance_to_boundary = min(self.x,self.y,x_size*10 - self.x, y_size*10 - self.y)
		if distance_to_boundary <= 50:
			self.ramp = (distance_to_boundary/30)
		else:
			self.ramp = 1

	#basically work out where you are relative to the moving body, if you are behind it then get a non-zero multiplier
	#that **10 is a bit horrible, maybe it's just easier to have a 45 degree bow-wave, not sure
	def set_moving_body(self):
		self.in_wake = 0		
		norm_motion = math.sqrt(Motion[0]**2 + Motion[1]**2)		
		relative_position = [Position[0] - self.x, Position[1] - self.y]
		if relative_position[0] <= 0:
			relative_position[0] = 0
			relative_position[1] = 0
		norm_relative_position = math.sqrt(relative_position[0]**2 + relative_position[1]**2)
		dot_product = (relative_position[0]*Motion[0] 
			+ relative_position[1]*Motion[1])/(0.1 + norm_motion*norm_relative_position)		
		self.in_wake = dot_product**10
		if norm_relative_position <= 50:
			self.in_wake = 0

	#generate noise for the potential field, this is where I don't really know what I'm doing
	def generate_psi(self):
		self.set_ramp()
		self.set_moving_body()
		noise = math.sin(math.sqrt((20 + time - i)**2 + (20 + time - j)**2))
		# bascially this is only not small if you are away from the boundary AND behind the moving sphere
		self.psi = self.ramp*self.in_wake*noise

	


#initialise
points = []

x_size = 100
y_size = 100

for i in range(x_size):
	points.append([])
	for j in range(y_size):
		points[i].append(point(i,j))

#motion and position for the moving sphere
Motion = [10,0]
Position = [200,200]


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
	if time >= 6*math.pi:
		time = 0

	#update and draw the moving sphere
	Position[0] = Position[0] + Motion[0]
	Position[1] = Position[1] + Motion[1]
	pygame.draw.circle(screen, (255,0,0), (Position[0],Position[1]),50, 5)

	pygame.display.flip()

pygame.quit()