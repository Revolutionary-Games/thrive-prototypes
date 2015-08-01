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

#standard distance between two points
def get_distance(point1, point2):
	return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

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
		self.mask = 0
		self.neighbours = []

	#who are my neighbours?
	def set_neighbours(self):
		if self.i >=1:
			self.neighbours.append(points[i-1][j])
		if self.j >=1:
			self.neighbours.append(points[i][j-1])
		if self.i <= x_size - 2:
			self.neighbours.append(points[i + 1][j])
		if self.j <= y_size - 2:
			self.neighbours.append(points[i][j + 1])


	def display(self):
		factor = 1
		#the line to draw is the underlying noise (self.dx & dy) reduced by the mask
		x_length = self.mask*factor*self.dx
		y_length = self.mask*factor*self.dy
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

	#reduce the amount of tubulence seen based on the mask. 
	def set_mask(self):
		#moving microbes add to the mask
		for microbe in microbes:
			if get_distance(self, microbe) <= 20:
				self. mask = 20*math.sqrt(microbe.dx**2 + microbe.dy**2)
		#average out your mask with your neighbours (diffusion)
		neighbours_masks_sum = 0
		number_of_neighbours = 0
		for neighbour in self.neighbours:
			neighbours_masks_sum += neighbour.mask
			number_of_neighbours += 1
		#0.999 here determines the speed of the diffusion, closer to 1 means faster
		self.mask += 0.999*((neighbours_masks_sum/(number_of_neighbours)) - self.mask)
		#mask decays over time
		self.mask *= 0.99
		#save computing power by cuttin off tiny floats
		if self.mask <= 0.02:
			self.mask = 0


#this is a super basic class to draw a red circle on the screen and make it move around randomly
class microbe:
	def __init__(self):
		self.x = random.randint(100,900)
		self.y = random.randint(100,500)
		self.speed = 10
		self.dx = random.uniform(-self.speed,self.speed)
		self.dy = random.uniform(-self.speed,self.speed)
		self.size = 30

	def display(self):
		pygame.draw.circle(screen, (255,0,0), (int(self.x), int(self.y)), self.size)

	def move(self):
		self.x += self.dx
		self.y += self.dy
		if time == 0:
			self.dx = random.uniform(-self.speed,self.speed)
			self.dy = random.uniform(-self.speed,self.speed)
		if self.x >= width:
			self.x -= width
		if self.x <= 0:
			self.x += width
		if self.y >= height:
			self.y -= height
		if self.y <= 0:
			self.y += height


#initialise
points = []
microbes = []

x_size = 100
y_size = 100

for i in range(x_size):
	points.append([])
	for j in range(y_size):
		points[i].append(point(i,j))

for i in range(x_size):
	for j in range(y_size):	
		points[i][j].set_neighbours()

number_of_microbes = 3

for i in range(number_of_microbes):
	microbes.append(microbe())


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

	#set mask for each point and then display
	for i in range(len(points)):
		for j in range(len(points[i])):
			points[i][j].set_mask()
			points[i][j].display()
			
	#move and display microbes
	for microbe in microbes:
		microbe.move()
		microbe.display()

	#time is what causes the noise to change
	time += 1
	if time >= 50:
		time = 0

	pygame.display.flip()

pygame.quit()