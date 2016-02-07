#prototype of combat gameplay

import pygame
import math
import random
from pygame.locals import *

#pygame setup
background_colour = (255,255,255)
(width, height) = (1000, 700)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Combat')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 30)

clock = pygame.time.Clock()

class agent:
	def __init__(self, position, code, parent):
		self.pos = position
		self.code = code
		self.parent = parent
		self.time = 0
		self.max_time = 100

	def display(self):
		pygame.draw.circle(screen, [0,255,0], [int(self.pos[0]), int(self.pos[1])], 300, 2)

	def age(self):
		self.time += 1
		if self.time >= self.max_time:
			agents.remove(self)
			self.parent.agent_counter = 1

	def wound(self):
		for microba in microbes:
			if collide(self.pos, microba.pos, 300):
				if microba.code[0] != self.code[0]:
					microba.health -= 1
				if microba.code[1] != self.code[1]:
					microba.speed = 1
				if microba.code[2] != self.code[2]:
					microba.agent_counter = 5
				if self not in microba.affected_by:
					microba.affected_by.append(self)



class microbe:
	def __init__(self, player = False):
		self.player = player
		if self.player: self.colour = [0,0,255]
		else: self.colour = [255,0,0]
		self.pos = [random.uniform(0,width), random.uniform(0,height)]
		self.vel = [0,0]
		if self.player:
			self.speed = 5
		else:
			self.speed = 2
		self.health = 45
		self.code = [random.randint(0,1),random.randint(0,1),random.randint(0,1)]
		self.agent_counter = 1
		self.agent_max = 1
		self.affected_by = []

	def display(self):
		pygame.draw.circle(screen, self.colour, [int(self.pos[0]), int(self.pos[1])], 50, 5)
		pygame.draw.circle(screen, [0,255,0], [int(self.pos[0]), int(self.pos[1])], int(self.health))

	def move(self, mouse_pos, wasd):
		if self.player == True:
			direction = get_vector_from_to(self.pos, mouse_pos)
			direction = normalise(direction)
			left = [direction[1],-direction[0]]
			if wasd == "w":
				self.vel = [self.speed*direction[0], self.speed*direction[1]]
			if wasd == "s":
				self.vel = [-self.speed*direction[0], -self.speed*direction[1]]
			if wasd == "a":
				self.vel = [self.speed*0.75*left[0], self.speed*0.75*left[1]]
			if wasd == "d":
				self.vel = [-self.speed*0.75*left[0], -self.speed*0.75*left[1]]
			if wasd == False: self.vel = [0,0]

		self.pos = addup(self.pos, self.vel)
		if self.pos[0] >= width:
			self.pos[0] -= width
		if self.pos[0] <= 0:
			self.pos[0] += width
		if self.pos[1] >= height:
			self.pos[1] -= height
		if self.pos[1] <= 0:
			self.pos[1] += height

	def drop_agent(self):
		agents.append(agent(self.pos, self.code, self))

	def check_self(self):
		if self.health <= 1:
			microbes.remove(self)
		for agenta in self.affected_by:
			if agenta not in agents:
				self.affected_by.remove(agenta)
				if self.player:
					self.speed = 5
				else:
					self.speed = 2
				self.agent_counter = 1


	def ai(self):
		for microba in microbes:
			if microba is not self:
				vector = normalise(get_vector_from_to(self.pos, microba.pos))
				self.vel = [self.speed*vector[0], self.speed*vector[1]]
			if microba.player and self.agent_counter <= self.agent_max:
				if collide(self.pos, microba.pos, 200):
					self.drop_agent()
					self.agent_counter += 1	



def addup(list1, list2):
	return [x + y for x, y in zip(list1, list2)]

def get_vector_from_to(list1, list2):
	return addup([-list1[0], -list1[1]], list2)

def norm(list1):
	value = math.sqrt(list1[0]**2 + list1[1]**2)
	if value == 0:
		value = 0.0001
	return value

def normalise(list1):
	norm_list1 = norm(list1)
	return [float(list1[0])/norm_list1, float(list1[1])/norm_list1]

def collide(list1, list2, distance):
	vector = get_vector_from_to(list1, list2)
	norm_vector = norm(vector)
	if norm_vector <= distance:
		return True
	else:
		return False 

microbes = []
agents = []

def setup():
	global microbes
	global agents
	microbes = []
	agents = []
	for i in range(random.choice([1,1,1,1,2,2,3])):
		microbes.append(microbe())
	microbes.append(microbe(player = True))
		

setup()

wasd = False
dropping_agent = False

pause = False
running = True
while running:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        running = False
	    elif event.type == KEYDOWN:
	        if event.key == K_ESCAPE:
	            running = False
	    	if event.key == K_SPACE:
	    		setup()
	        	

	screen.fill(background_colour)

	mouse_pos = pygame.mouse.get_pos()

	keys_pressed = pygame.key.get_pressed()

	if keys_pressed[K_w]: wasd = "w"
	elif keys_pressed[K_a]: wasd = "a"
	elif keys_pressed[K_s]: wasd = "s"
	elif keys_pressed[K_d]: wasd = "d"
	else: wasd = False

	if keys_pressed[K_e]:
		dropping_agent = True
	else:
		dropping_agent = False

	for microba in microbes:
		microba.move(mouse_pos, wasd)
		microba.display()
		microba.check_self()
		if dropping_agent and microba.player and microba.agent_counter <= microba.agent_max:
			microba.drop_agent()
			microba.agent_counter += 1
		if not microba.player:
			microba.ai()

	for agenta in agents:
		agenta.display()
		agenta.age()
		agenta.wound()


	pygame.display.flip()

	clock.tick(60)
	        
pygame.quit()