import pygame
import math
import random
from pygame.locals import *

clock = pygame.time.Clock()

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
		factor = 1
		#the line to draw is the underlying noise (self.dx & dy) reduced by the mask
		x_length = factor*self.dx
		y_length = factor*self.dy
		pygame.draw.line(screen, (0,0,255), 
			(int(scale*self.x), int(scale*self.y)), 
			(int(scale*self.x + x_length), int(scale*self.y + y_length)), 1)

	#get the vector field from the potential field, turns out it's super simple
	def generate_vector_field(self):
		self.dy = -get_derivative(self, points[self.i + 1][self.j])
		self.dx = get_derivative(self, points[self.i][self.j + 1])

	#generate noise for the potential field, this is where I don't really know what I'm doing
	def generate_psi(self):
		noise = math.sin(time*self.i*self.j/50)
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

	clock.tick()


	#generate the potential field and from it the vector field
	for i in range(x_size - 1):
		for j in range(y_size - 1):
			points[i][j].generate_psi()
			points[i][j].generate_vector_field()

	#set mask for each point and then display
	for i in range(len(points)):
		for j in range(len(points[i])):
			points[i][j].display()

	#time is what causes the noise to change
	time += 1
	if time >= 50:
		time = 0
		print clock.get_fps()


	pygame.display.flip()

pygame.quit()