# Proceedural tree generator, press SPACE to generate a new tree


import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (255,255,255)
(width, height) = (1600, 800)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Trees')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

#base variables
junctions_per_branch = 3
base_length = 200
reduction_factor = 0.75
angle_change = math.pi/4
max_generation = 7

#where to center the display
X_shift = width/2
Y_shift = height

trunk_colour = (160,82,45)
leaf_colour = (34,139,34)

class branch:
	def __init__(self, junction = None):
		#if this branch is the trunk
		self.start_x = 0
		self.start_y = 0
		self.start_z = 0
		self.end_x = 0
		self.end_y = 0
		self.end_z = base_length
		self.generation = 1
		self.length = base_length
		self.phi = 0
		self.theta = 0
		self.number_of_children = 0

		#if this branch is coming off a junction
		if junction:
			self.generation = junction.generation + 1
			self.length = base_length*(reduction_factor**self.generation)
			self.theta = junction.theta + random.uniform(-angle_change, + angle_change)
			self.phi = junction.phi + random.uniform(-angle_change, + angle_change)
			self.start_x = junction.x
			self.start_y = junction.y
			self.start_z = junction.z
			self.end_x = self.start_x +  self.length*math.sin(self.theta)*math.cos(self.phi)
			self.end_y = self.start_y +  self.length*math.sin(self.theta)*math.sin(self.phi)
			self.end_z = self.start_z +  self.length*math.cos(self.theta)
			self.number_of_children = 0
			


	def display(self, rotation):
		screen_x_0 = math.cos(rotation)*self.start_x + math.sin(rotation)*self.start_y
		screen_x_1 = math.sin(rotation)*self.end_y + math.cos(rotation)*self.end_x
		pygame.draw.line(screen, trunk_colour, [int(screen_x_0 + X_shift), int(-self.start_z + Y_shift)],
			[int(screen_x_1 + X_shift),int(- self.end_z + Y_shift)], int(20*(reduction_factor**self.generation)))


# a place where one brach comes off another
class junction:
	def __init__(self, branch):
		self.generation = branch.generation
		self.theta = branch.theta
		self.phi = branch.phi
		step = 1.0/junctions_per_branch

		self.x = branch.end_x + step*branch.number_of_children*(branch.start_x - branch.end_x)
		self.y = branch.end_y + step*branch.number_of_children*(branch.start_y - branch.end_y)
		self.z = branch.end_z + step*branch.number_of_children*(branch.start_z - branch.end_z)

		branch.number_of_children += 1

class leaf:
	def __init__(self, junction):
		self.x = junction.x
		self.y = junction.y
		self.z = junction.z 

	def display(self, rotation):
		screen_x_0 = math.cos(rotation)*self.x + math.sin(rotation)*self.y
		pygame.draw.circle(screen, leaf_colour, (int(screen_x_0 + X_shift), int(-self.z + Y_shift)),5)



def mainloop():
	global branches
	global leaves
	branches = []
	junctions = []

	branches.append(branch())

	current_generation = 1

	while current_generation <=  max_generation:
		#for every junction add a branch
		for i in junctions:
			branches.append(branch(i))
		junctions = []

		#for each branch keep adding junctions until they all have the right number
		repeat = True
		while repeat:
			found_one = False
			for i in branches:
				if i. generation == current_generation and i.number_of_children <= junctions_per_branch - 1:
					junctions.append(junction(i))
					found_one = True
			if not found_one:
				repeat = False

		current_generation += 1

	leaves = []

	for i in junctions:
		leaves.append(leaf(i))



	


mainloop()

running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	        if event.key == K_SPACE:
	        	mainloop()

	screen.fill(background_colour)

	pos = pygame.mouse.get_pos()
	rotation = float(pos[0])/300

	for i in branches:
		i.display(rotation)
	for i in leaves:
		i.display(rotation)

	pygame.display.flip()
	

pygame.quit()